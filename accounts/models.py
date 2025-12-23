from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from djangoblog.utils import get_current_site


# Create your models here.

class BlogUser(AbstractUser):
    nickname = models.CharField(_('nick name'), max_length=100, blank=True)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)
    source = models.CharField(_('create source'), max_length=100, blank=True)

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

    class Meta:
        ordering = ['-id']
        verbose_name = _('user')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'


class Notification(models.Model):
    """通知模型"""
    TYPE_CHOICES = (
        ('comment_reply', _('Comment Reply')),
        ('system_notice', _('System Notice')),
        ('article_approve', _('Article Approve')),
        ('article_reject', _('Article Reject')),
    )
    
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES, default='system_notice')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE)
    is_read = models.BooleanField(_('is read'), default=False)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    
    # 关联对象（可选）
    related_object_id = models.PositiveIntegerField(_('related object id'), blank=True, null=True)
    related_object_type = models.CharField(_('related object type'), max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ['-creation_time']
        verbose_name = _('notification')
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.title
    
    def mark_as_read(self):
        """标记为已读"""
        if not self.is_read:
            self.is_read = True
            self.save()
    
    def get_absolute_url(self):
        """获取通知的绝对URL"""
        if self.related_object_type == 'article' and self.related_object_id:
            from blog.models import Article
            try:
                article = Article.objects.get(pk=self.related_object_id)
                return article.get_absolute_url()
            except Article.DoesNotExist:
                return reverse('blog:index')
        return reverse('blog:index')
