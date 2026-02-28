from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Register your models here.
from .models import Article, Category, Tag, Links, SideBar, BlogSettings, ArticleVersion


class ArticleForm(forms.ModelForm):
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


makr_article_publish.short_description = _('Publish selected articles')
draft_article.short_description = _('Draft selected articles')
close_article_commentstatus.short_description = _('Close article comments')
open_article_commentstatus.short_description = _('Open article comments')


class ArticlelAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('body', 'title')
    form = ArticleForm
    list_display = (
        'id',
        'title',
        'author',
        'link_to_category',
        'creation_time',
        'views',
        'status',
        'type',
        'article_order')
    list_display_links = ('id', 'title')
    list_filter = ('status', 'type', 'category')
    date_hierarchy = 'creation_time'
    filter_horizontal = ('tags',)
    exclude = ('creation_time', 'last_modify_time')
    view_on_site = True
    actions = [
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
        # 传递 request 参数给 save 方法，以便获取当前用户
        obj.save(request=request)

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


class ArticleVersionAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('title', 'body')
    list_display = (
        'id',
        'article_title',
        'version_number',
        'editor',
        'creation_time',
        'comment',
        'restore_link'
    )
    list_display_links = ('id', 'article_title')
    list_filter = ('editor', 'creation_time')
    date_hierarchy = 'creation_time'
    readonly_fields = ('article', 'version_number', 'title', 'body', 'editor', 'creation_time', 'last_modify_time')
    exclude = ('last_modify_time',)

    def article_title(self, obj):
        return format_html(u'<a href="%s">%s</a>' % (
            reverse('admin:blog_article_change', args=(obj.article.id,)),
            obj.article.title
        ))
    article_title.short_description = _('article title')

    def restore_link(self, obj):
        return format_html(u'<a href="%s" onclick="return confirm(\'确定要恢复到此版本吗？\')">%s</a>' % (
            reverse('admin:restore_version', args=(obj.id,)),
            _('Restore this version')
        ))
    restore_link.short_description = _('restore operation')


@admin.action(description=_('Restore selected version'))
def restore_version_action(modeladmin, request, queryset):
    for version in queryset[:1]:  # 只恢复第一个选中的版本
        article = version.article
        # 先保存当前版本作为历史记录
        last_version = article.versions.order_by('-version_number').first()
        new_version_number = last_version.version_number + 1 if last_version else 1
        
        ArticleVersion.objects.create(
            article=article,
            version_number=new_version_number,
            title=article.title,
            body=article.body,
            editor=request.user,
            comment=_('Backup before restoration')
        )
        
        # 恢复版本内容
        article.title = version.title
        article.body = version.body
        article.save(request=request)
        break


@admin.action(description=_('Compare selected versions'))
def compare_versions_action(modeladmin, request, queryset):
    if len(queryset) != 2:
        modeladmin.message_user(request, _('Please select exactly two versions to compare'), level='error')
        return
    
    version_ids = [str(version.id) for version in queryset]
    return HttpResponseRedirect(
        reverse('admin:compare_versions') + f'?v1={version_ids[0]}&v2={version_ids[1]}'
    )


from .utils.diff import get_version_diff

# 注册恢复版本的URL
from django.urls import path
from django.template.response import TemplateResponse

class ArticleVersionAdminWithURL(ArticleVersionAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('restore/<int:version_id>/', self.admin_site.admin_view(self.restore_view), name='restore_version'),
            path('compare/', self.admin_site.admin_view(self.compare_view), name='compare_versions'),
        ]
        return custom_urls + urls

    def restore_view(self, request, version_id):
        version = get_object_or_404(ArticleVersion, id=version_id)
        article = version.article
        
        # 先保存当前版本作为历史记录
        last_version = article.versions.order_by('-version_number').first()
        new_version_number = last_version.version_number + 1 if last_version else 1
        
        ArticleVersion.objects.create(
            article=article,
            version_number=new_version_number,
            title=article.title,
            body=article.body,
            editor=request.user,
            comment=_('Backup before restoration')
        )
        
        # 恢复版本内容
        article.title = version.title
        article.body = version.body
        article.save(request=request)
        
        self.message_user(request, _('Successfully restored to version %d') % version.version_number)
        return HttpResponseRedirect(reverse('admin:blog_article_change', args=(article.id,)))
    
    def compare_view(self, request):
        version1_id = request.GET.get('v1')
        version2_id = request.GET.get('v2')
        
        if not version1_id or not version2_id:
            self.message_user(request, _('Please select two versions to compare'), level='error')
            return HttpResponseRedirect(reverse('admin:blog_articleversion_changelist'))
        
        version1 = get_object_or_404(ArticleVersion, id=version1_id)
        version2 = get_object_or_404(ArticleVersion, id=version2_id)
        
        # 确保两个版本属于同一篇文章
        if version1.article.id != version2.article.id:
            self.message_user(request, _('Cannot compare versions from different articles'), level='error')
            return HttpResponseRedirect(reverse('admin:blog_articleversion_changelist'))
        
        diff_data = get_version_diff(version1, version2)
        
        context = dict(
            self.admin_site.each_context(request),
            title=_('Compare Version %(v1)s vs %(v2)s') % {'v1': version1.version_number, 'v2': version2.version_number},
            diff_data=diff_data,
            opts=self.model._meta,
        )
        
        return TemplateResponse(request, 'admin/compare_versions.html', context)

ArticleVersionAdminWithURL.actions = [restore_version_action, compare_versions_action]


class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', 'last_mod_time', 'creation_time')


class LinksAdmin(admin.ModelAdmin):
    exclude = ('last_mod_time', 'creation_time')


class SideBarAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'is_enable', 'sequence')
    exclude = ('last_mod_time', 'creation_time')


class BlogSettingsAdmin(admin.ModelAdmin):
    pass



admin.site.register(Article, ArticlelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(SideBar, SideBarAdmin)
admin.site.register(BlogSettings, BlogSettingsAdmin)
admin.site.register(ArticleVersion, ArticleVersionAdminWithURL)
