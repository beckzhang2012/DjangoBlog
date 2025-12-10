from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from djangoblog.utils import get_current_site


# Create your models here.
class BlogUser(AbstractUser):
    nickname = models.CharField(_('nick name'), max_length=100, blank=True)
    source = models.CharField(_('create source'), max_length=100, blank=True)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)

    def get_absolute_url(self):
        return reverse(
            'blog:author_detail', kwargs={
                'author_name': self.username})

    def __str__(self):
        return self.email
    
    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site,
                                            path=self.get_absolute_url())
        return url

    def get_unread_notifications_count(self):
        """获取未读消息数量"""
        return Notification.objects.filter(recipient=self, is_read=False).count()
    
    class Meta:
        ordering = ['-id']
        verbose_name = _('user')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'


class Notification(models.Model):
    """消息通知模型"""
    NOTIFICATION_TYPES = (
        ('comment_reply', '评论回复'),
        ('system_notice', '系统通知'),
        ('article_approved', '文章审核通过'),
        ('article_rejected', '文章审核拒绝'),
    )
    
    recipient = models.ForeignKey(
        BlogUser,
        verbose_name=_('接收用户'),
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    sender = models.ForeignKey(
        BlogUser,
        verbose_name=_('发送用户'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sent_notifications'
    )
    title = models.CharField(_('通知标题'), max_length=200)
    content = models.TextField(_('通知内容'))
    notification_type = models.CharField(
        _('通知类型'),
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='system_notice'
    )
    target_url = models.CharField(_('跳转链接'), max_length=500, blank=True)
    is_read = models.BooleanField(_('已读'), default=False)
    created_time = models.DateTimeField(_('创建时间'), default=now)
    
    class Meta:
        ordering = ['-created_time']
        verbose_name = _('通知')
        verbose_name_plural = _('通知')
    
    def __str__(self):
        return f"{self.get_notification_type_display()}: {self.title}"
    
    def mark_as_read(self):
        """标记为已读"""
        if not self.is_read:
            self.is_read = True
            self.save()
    
    def get_absolute_url(self):
        """获取通知绝对URL"""
        return reverse('notification_detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-created_time']
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
