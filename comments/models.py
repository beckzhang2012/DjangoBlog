from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# 解决循环导入问题，使用字符串引用


# 审核状态枚举
class AuditStatus(models.TextChoices):
    PENDING = ('pending', _('Pending Review'))
    APPROVED = ('approved', _('Approved'))
    REJECTED = ('rejected', _('Rejected'))
    NEED_MODIFICATION = ('modify', _('Need Modification'))


# 审核类型枚举
class AuditType(models.TextChoices):
    COMMENT = ('comment', _('Comment'))
    ARTICLE = ('article', _('Article'))


class AuditLog(models.Model):
    """审核日志模型"""
    content_type = models.CharField(
        max_length=20,
        choices=AuditType.choices,
        verbose_name=_('Audit Type'),
        help_text=_('Comment or Article'),
        default=AuditType.COMMENT
    )
    content_id = models.IntegerField(verbose_name=_('Content ID'))
    original_content = models.TextField(verbose_name=_('Original Content'), blank=True)
    audit_status = models.CharField(
        _('audit status'),
        max_length=20,
        choices=AuditStatus.choices,
        default=AuditStatus.PENDING
    )
    audit_opinion = models.TextField(_('audit opinion'), blank=True, null=True)
    auditor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('auditor'),
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    audit_time = models.DateTimeField(_('audit time'), default=now)
    creation_time = models.DateTimeField(_('creation time'), default=now)

    class Meta:
        ordering = ['-audit_time']
        verbose_name = _('audit log')
        verbose_name_plural = _('audit logs')

    def __str__(self):
        return f"{self.get_content_type_display()} {self.content_id} - {self.get_audit_status_display()}"


class Comment(models.Model):
    body = models.TextField('正文', max_length=300)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        on_delete=models.CASCADE)
    article = models.ForeignKey(
        'blog.Article',
        verbose_name=_('article'),
        on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        'self',
        verbose_name=_('parent comment'),
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    audit_status = models.CharField(
        _('audit status'),
        max_length=20,
        choices=AuditStatus.choices,
        default=AuditStatus.PENDING
    )
    is_enable = models.BooleanField(_('enable'),
                                    default=False, blank=False, null=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _('comment')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def __str__(self):
        return self.body
