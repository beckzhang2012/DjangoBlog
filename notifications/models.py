from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class NotificationType(models.TextChoices):
    COMMENT_REPLY = 'comment_reply', _('评论回复')
    SYSTEM_NOTICE = 'system_notice', _('系统通知')
    ARTICLE_REVIEW = 'article_review', _('文章审核')


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('接收者'),
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('发送者'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sent_notifications'
    )
    title = models.CharField(_('通知标题'), max_length=200)
    content = models.TextField(_('通知内容'))
    notification_type = models.CharField(
        _('通知类型'),
        max_length=50,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM_NOTICE
    )
    is_read = models.BooleanField(_('已读'), default=False)
    created_time = models.DateTimeField(_('创建时间'), default=now)
    url = models.URLField(_('跳转链接'), max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name = _('通知')
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()