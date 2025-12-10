from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from blog.models import Article


# Create your models here.

class AuditStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    APPROVED = 'approved', _('Approved')
    REJECTED = 'rejected', _('Rejected')
    NEED_MODIFICATION = 'need_modification', _('Need Modification')


class Comment(models.Model):
    body = models.TextField('正文', max_length=300)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article,
        verbose_name=_('article'),
        on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        'self',
        verbose_name=_('parent comment'),
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    is_enable = models.BooleanField(_('enable'),
                                    default=False, blank=False, null=False)
    audit_status = models.CharField(
        _('audit status'),
        max_length=20,
        choices=AuditStatus.choices,
        default=AuditStatus.PENDING,
        help_text=_('Comment audit status')
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _('comment')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def __str__(self):
        return self.body


class CommentAuditHistory(models.Model):
    comment = models.ForeignKey(
        Comment,
        verbose_name=_('comment'),
        on_delete=models.CASCADE,
        related_name='audit_histories'
    )
    auditor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('auditor'),
        on_delete=models.CASCADE
    )
    audit_time = models.DateTimeField(_('audit time'), default=now)
    old_status = models.CharField(
        _('old status'),
        max_length=20,
        choices=AuditStatus.choices
    )
    new_status = models.CharField(
        _('new status'),
        max_length=20,
        choices=AuditStatus.choices
    )
    audit_opinion = models.TextField(
        _('audit opinion'),
        max_length=500,
        blank=True,
        null=True,
        help_text=_('Auditor comments and opinions')
    )

    class Meta:
        ordering = ['-audit_time']
        verbose_name = _('comment audit history')
        verbose_name_plural = _('comment audit histories')

    def __str__(self):
        return f"{self.auditor.username} - {self.old_status} → {self.new_status} at {self.audit_time}"
