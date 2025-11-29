from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _


class NotificationType(models.TextChoices):
    COMMENT_REPLY = 'comment_reply', _('Comment Reply')
    SYSTEM = 'system', _('System Notification')
    AUDIT = 'audit', _('Article Approval')


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Recipient')
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications',
        verbose_name=_('Sender')
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        verbose_name=_('Notification Type')
    )
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    content = models.TextField(_('Content'))
    related_object_id = models.BigIntegerField(null=True, blank=True, verbose_name=_('Related Object ID'))
    related_content_type_id = models.IntegerField(null=True, blank=True, verbose_name=_('Related Content Type ID'))
    is_read = models.IntegerField(default=0, verbose_name=_('Is Read'))
    read_time = models.DateTimeField(null=True, blank=True, verbose_name=_('Read Time'))
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_('Extra Data'))

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-creation_time']

    def __str__(self):
        return f"Notification for {self.recipient}: {self.title[:50]}..."