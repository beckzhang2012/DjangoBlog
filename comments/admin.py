from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Comment, AuditLog, AuditStatus, AuditType


def approve_comments(modeladmin, request, queryset):
    for comment in queryset:
        comment.audit_status = AuditStatus.APPROVED
        comment.is_enable = True
        comment.save()
        # 创建审核日志
        AuditLog.objects.create(
            content_type=AuditType.COMMENT,
            content_id=comment.id,
            original_content=comment.body,
            audit_status=AuditStatus.APPROVED,
            auditor=request.user
        )
    messages.success(request, _('Successfully approved selected comments'))


def reject_comments(modeladmin, request, queryset):
    for comment in queryset:
        comment.audit_status = AuditStatus.REJECTED
        comment.is_enable = False
        comment.save()
        # 创建审核日志
        AuditLog.objects.create(
            content_type=AuditType.COMMENT,
            content_id=comment.id,
            original_content=comment.body,
            audit_status=AuditStatus.REJECTED,
            auditor=request.user
        )
    messages.success(request, _('Successfully rejected selected comments'))


def need_modification_comments(modeladmin, request, queryset):
    for comment in queryset:
        comment.audit_status = AuditStatus.NEED_MODIFICATION
        comment.is_enable = False
        comment.save()
        # 创建审核日志
        AuditLog.objects.create(
            content_type=AuditType.COMMENT,
            content_id=comment.id,
            original_content=comment.body,
            audit_status=AuditStatus.NEED_MODIFICATION,
            auditor=request.user
        )
    messages.success(request, _('Successfully marked selected comments as needing modification'))


def disable_commentstatus(modeladmin, request, queryset):
    queryset.update(is_enable=False)


def enable_commentstatus(modeladmin, request, queryset):
    queryset.update(is_enable=True)


approve_comments.short_description = _('Approve selected comments')
reject_comments.short_description = _('Reject selected comments')
need_modification_comments.short_description = _('Mark as needing modification')
disable_commentstatus.short_description = _('Disable comments')
enable_commentstatus.short_description = _('Enable comments')





class CommentAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id',
        'body',
        'link_to_userinfo',
        'link_to_article',
        'audit_status',
        'is_enable',
        'creation_time')
    list_display_links = ('id', 'body')
    list_filter = ('audit_status', 'is_enable', 'creation_time')
    exclude = ('creation_time', 'last_modify_time')
    actions = [approve_comments, reject_comments, need_modification_comments, disable_commentstatus, enable_commentstatus]
    raw_id_fields = ('author', 'article')
    search_fields = ('body', 'author__username', 'author__email', 'article__title')
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is not None and request.user.is_staff:
            # 动态添加审核意见字段
            form.base_fields['audit_opinion'] = forms.CharField(
                widget=forms.Textarea(attrs={'rows': 3}),
                required=False,
                label=_('Audit Opinion')
            )
        return form

    def save_model(self, request, obj, form, change):
        if change and 'audit_status' in form.changed_data:
            # 创建审核日志
            AuditLog.objects.create(
                content_type=AuditType.COMMENT,
                content_id=obj.id,
                original_content=obj.body,
                audit_status=obj.audit_status,
                audit_opinion=form.cleaned_data.get('audit_opinion'),
                auditor=request.user
            )
            # 根据审核状态设置是否启用
            if obj.audit_status == AuditStatus.APPROVED:
                obj.is_enable = True
            else:
                obj.is_enable = False
        super().save_model(request, obj, form, change)

    def link_to_userinfo(self, obj):
        info = (obj.author._meta.app_label, obj.author._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.author.id,))
        return format_html(
            u'<a href="%s">%s</a>' %
            (link, obj.author.nickname if obj.author.nickname else obj.author.email))

    def link_to_article(self, obj):
        info = (obj.article._meta.app_label, obj.article._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.article.id,))
        return format_html(
            u'<a href="%s">%s</a>' % (link, obj.article.title))

    link_to_userinfo.short_description = _('User')
    link_to_article.short_description = _('Article')


class AuditLogAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id',
        'content_type',
        'content_id',
        'audit_status',
        'auditor',
        'audit_time'
    )
    list_filter = ('content_type', 'audit_status', 'audit_time')
    search_fields = ('content_id', 'auditor__username', 'audit_opinion')
    readonly_fields = ('content_type', 'content_id', 'original_content', 'audit_status', 'audit_opinion', 'auditor', 'audit_time', 'creation_time')
    ordering = ['-audit_time']

    def has_add_permission(self, request):
        return False


admin.site.register(AuditLog, AuditLogAdmin)
