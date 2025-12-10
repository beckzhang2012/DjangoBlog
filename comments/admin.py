from django.contrib import admin
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Comment, AuditStatus, CommentAuditHistory
from .dashboard import CommentAuditDashboard


def disable_commentstatus(modeladmin, request, queryset):
    queryset.update(is_enable=False)


def enable_commentstatus(modeladmin, request, queryset):
    queryset.update(is_enable=True)


def approve_comments(modeladmin, request, queryset):
    for comment in queryset:
        old_status = comment.audit_status
        comment.audit_status = AuditStatus.APPROVED
        comment.is_enable = True
        comment.save()
        # Record audit history
        CommentAuditHistory.objects.create(
            comment=comment,
            auditor=request.user,
            old_status=old_status,
            new_status=AuditStatus.APPROVED,
            audit_opinion='批量通过审核'
        )
    messages.success(request, f"成功通过 {queryset.count()} 条评论")


def reject_comments(modeladmin, request, queryset):
    for comment in queryset:
        old_status = comment.audit_status
        comment.audit_status = AuditStatus.REJECTED
        comment.is_enable = False
        comment.save()
        # Record audit history
        CommentAuditHistory.objects.create(
            comment=comment,
            auditor=request.user,
            old_status=old_status,
            new_status=AuditStatus.REJECTED,
            audit_opinion='批量拒绝审核'
        )
    messages.success(request, f"成功拒绝 {queryset.count()} 条评论")


def need_modification_comments(modeladmin, request, queryset):
    for comment in queryset:
        old_status = comment.audit_status
        comment.audit_status = AuditStatus.NEED_MODIFICATION
        comment.is_enable = False
        comment.save()
        # Record audit history
        CommentAuditHistory.objects.create(
            comment=comment,
            auditor=request.user,
            old_status=old_status,
            new_status=AuditStatus.NEED_MODIFICATION,
            audit_opinion='需要修改'
        )
    messages.success(request, f"成功标记 {queryset.count()} 条评论为需要修改")


disable_commentstatus.short_description = _('Disable comments')
enable_commentstatus.short_description = _('Enable comments')
approve_comments.short_description = _('Approve selected comments')
reject_comments.short_description = _('Reject selected comments')
need_modification_comments.short_description = _('Mark as need modification')


class CommentAuditForm(forms.ModelForm):
    audit_opinion = forms.CharField(
        label=_('Audit Opinion'),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text=_('Optional: Add comments about this audit decision')
    )
    audit_status = forms.ChoiceField(
        label=_('Audit Status'),
        choices=AuditStatus.choices,
        required=True
    )

    class Meta:
        model = Comment
        fields = ['audit_status', 'is_enable', 'audit_opinion']


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
    actions = [approve_comments, reject_comments, need_modification_comments, enable_commentstatus, disable_commentstatus]
    raw_id_fields = ('author', 'article')
    search_fields = ('body', 'author__username', 'author__nickname', 'article__title')
    form = CommentAuditForm

    def changelist_view(self, request, extra_context=None):
        # Add pending count to the context
        pending_count = Comment.objects.filter(audit_status=AuditStatus.PENDING).count()
        extra_context = extra_context or {}
        extra_context['pending_count'] = pending_count
        return super().changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        if change and 'audit_status' in form.changed_data:
            # Record audit history when status changes
            old_status = Comment.objects.get(pk=obj.pk).audit_status
            new_status = obj.audit_status
            
            # Update is_enable based on audit status
            if new_status == AuditStatus.APPROVED:
                obj.is_enable = True
            elif new_status in [AuditStatus.REJECTED, AuditStatus.NEED_MODIFICATION]:
                obj.is_enable = False
                
            CommentAuditHistory.objects.create(
                comment=obj,
                auditor=request.user,
                old_status=old_status,
                new_status=new_status,
                audit_opinion=form.cleaned_data.get('audit_opinion', '')
            )
            messages.success(request, f"审核状态已更新为 {obj.get_audit_status_display()}")
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


class CommentAuditHistoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id',
        'link_to_comment',
        'link_to_auditor',
        'old_status',
        'new_status',
        'audit_time',
        'audit_opinion_preview'
    )
    list_display_links = ('id',)
    list_filter = ('old_status', 'new_status', 'audit_time')
    search_fields = (
        'comment__body',
        'auditor__username',
        'auditor__nickname',
        'audit_opinion'
    )
    readonly_fields = (
        'comment',
        'auditor',
        'old_status',
        'new_status',
        'audit_time',
        'audit_opinion'
    )
    date_hierarchy = 'audit_time'

    def link_to_comment(self, obj):
        info = (obj.comment._meta.app_label, obj.comment._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.comment.id,))
        return format_html(u'<a href="%s">%s</a>' % (link, obj.comment.body[:50] + '...'))

    def link_to_auditor(self, obj):
        info = (obj.auditor._meta.app_label, obj.auditor._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.auditor.id,))
        return format_html(
            u'<a href="%s">%s</a>' %
            (link, obj.auditor.nickname if obj.auditor.nickname else obj.auditor.username))
    
    def audit_opinion_preview(self, obj):
        if obj.audit_opinion:
            return obj.audit_opinion[:100] + '...' if len(obj.audit_opinion) > 100 else obj.audit_opinion
        return '-'

    link_to_comment.short_description = _('Comment')
    link_to_auditor.short_description = _('Auditor')
    audit_opinion_preview.short_description = _('Audit Opinion Preview')


class CommentAuditStats(CommentAuditDashboard):
    model = Comment


# Create a simple proxy model for dashboard
from django.db import models

class CommentAuditProxy(Comment):
    class Meta:
        proxy = True
        verbose_name = _('Comment Audit Dashboard')
        verbose_name_plural = _('Comment Audit Dashboard')


admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentAuditHistory, CommentAuditHistoryAdmin)
admin.site.register(CommentAuditProxy, CommentAuditStats)

# Custom admin site configuration
admin.site.index_title = _('Blog Administration')
admin.site.site_header = _('Blog Admin')
admin.site.site_title = _('Blog Admin Portal')
