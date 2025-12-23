from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """通知模型"""
    NOTIFICATION_TYPES = (
        ('comment_reply', _('Comment Reply')),
        ('system_notice', _('System Notice')),
        ('article_approved', _('Article Approved')),
    )
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Recipient'),
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Sender'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications'
    )
    
    title = models.CharField(_('Title'), max_length=200)
    content = models.TextField(_('Content'))
    notification_type = models.CharField(
        _('Notification Type'),
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='comment_reply'
    )
    
    target_url = models.URLField(_('Target URL'), blank=True, null=True)
    is_read = models.BooleanField(_('Is Read'), default=False)
    created_at = models.DateTimeField(_('Created At'), default=now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
    
    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.recipient.username}"
    
    def mark_as_read(self):
        """标记为已读"""
        if not self.is_read:
            self.is_read = True
            self.save()
    
    def mark_as_unread(self):
        """标记为未读"""
        if self.is_read:
            self.is_read = False
            self.save()