from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

# Register your models here.
from .models import Article, Category, Tag, Links, SideBar, BlogSettings
from comments.models import AuditStatus, AuditLog, AuditType


class ArticleForm(forms.ModelForm):
    audit_opinion = forms.CharField(widget=forms.Textarea, required=False, label=_('Audit Opinion'))
    audit_status = forms.ChoiceField(choices=AuditStatus.choices, label=_('Audit Status'))
    
    # body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Article
        fields = '__all__'


def makr_article_publish(modeladmin, request, queryset):
    queryset.update(status='p')


def draft_article(modeladmin, request, queryset):
    queryset.update(status='d')


def close_article_commentstatus(modeladmin, request, queryset):
    queryset.update(comment_status='c')


def open_article_commentstatus(modeladmin, request, queryset):
    queryset.update(comment_status='o')


def approve_articles(modeladmin, request, queryset):
    for article in queryset:
        article.audit_status = AuditStatus.APPROVED
        article.status = 'p'
        article.save()
        # 创建审核日志
        AuditLog.objects.create(
            content_type=AuditType.ARTICLE,
            content_id=article.id,
            original_content=article.title + '\n' + article.body[:200] + '...',
            audit_status=AuditStatus.APPROVED,
            auditor=request.user
        )
    messages.success(request, _('Successfully approved selected articles'))


def reject_articles(modeladmin, request, queryset):
    for article in queryset:
        article.audit_status = AuditStatus.REJECTED
        article.status = 'd'
        article.save()
        # 创建审核日志
        AuditLog.objects.create(
            content_type=AuditType.ARTICLE,
            content_id=article.id,
            original_content=article.title + '\n' + article.body[:200] + '...',
            audit_status=AuditStatus.REJECTED,
            auditor=request.user
        )
    messages.success(request, _('Successfully rejected selected articles'))


def need_modification_articles(modeladmin, request, queryset):
    for article in queryset:
        article.audit_status = AuditStatus.NEED_MODIFICATION
        article.status = 'd'
        article.save()
        # 创建审核日志
        AuditLog.objects.create(
            content_type=AuditType.ARTICLE,
            content_id=article.id,
            original_content=article.title + '\n' + article.body[:200] + '...',
            audit_status=AuditStatus.NEED_MODIFICATION,
            auditor=request.user
        )
    messages.success(request, _('Successfully marked selected articles as needing modification'))


makr_article_publish.short_description = _('Publish selected articles')
draft_article.short_description = _('Draft selected articles')
close_article_commentstatus.short_description = _('Close article comments')
open_article_commentstatus.short_description = _('Open article comments')
approve_articles.short_description = _('Approve selected articles')
reject_articles.short_description = _('Reject selected articles')
need_modification_articles.short_description = _('Mark as needing modification')


class ArticlelAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('body', 'title', 'author__username', 'author__email')
    form = ArticleForm
    list_display = (
        'id',
        'title',
        'author',
        'link_to_category',
        'creation_time',
        'views',
        'status',
        'audit_status',
        'type',
        'article_order')
    list_display_links = ('id', 'title')
    list_filter = ('status', 'audit_status', 'type', 'category')
    date_hierarchy = 'creation_time'
    filter_horizontal = ('tags',)
    exclude = ('creation_time', 'last_modify_time')
    view_on_site = True
    actions = [
        approve_articles,
        reject_articles,
        need_modification_articles,
        makr_article_publish,
        draft_article,
        close_article_commentstatus,
        open_article_commentstatus]
    raw_id_fields = ('author', 'category',)

    def link_to_category(self, obj):
        info = (obj.category._meta.app_label, obj.category._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.category.id,))
        return format_html(u'<a href="%s">%s</a>' % (link, obj.category.name))

    link_to_category.short_description = _('category')

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticlelAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].queryset = get_user_model(
        ).objects.filter(is_superuser=True)
        return form

    def save_model(self, request, obj, form, change):
        if change and 'audit_status' in form.changed_data:
            # 创建审核日志
            AuditLog.objects.create(
                content_type=AuditType.ARTICLE,
                content_id=obj.id,
                original_content=obj.title + '\n' + obj.body[:200] + '...',
                audit_status=obj.audit_status,
                audit_opinion=form.cleaned_data.get('audit_opinion'),
                auditor=request.user
            )
            # 根据审核状态设置发布状态
            if obj.audit_status == AuditStatus.APPROVED:
                obj.status = 'p'
            else:
                obj.status = 'd'
        super(ArticlelAdmin, self).save_model(request, obj, form, change)

    def get_view_on_site_url(self, obj=None):
        if obj:
            url = obj.get_full_url()
            return url
        else:
            from djangoblog.utils import get_current_site
            site = get_current_site().domain
            return site


class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', 'last_mod_time', 'creation_time')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'index')
    exclude = ('slug', 'last_mod_time', 'creation_time')


class LinksAdmin(admin.ModelAdmin):
    exclude = ('last_mod_time', 'creation_time')


class SideBarAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'is_enable', 'sequence')
    exclude = ('last_mod_time', 'creation_time')


class BlogSettingsAdmin(admin.ModelAdmin):
    pass
