from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from djangoblog.utils import cache_decorator, cache


class Comment(models.Model):
    STATUS_CHOICES = (
        ('n', _('New')),
        ('a', _('Approved')),
        ('r', _('Rejected')),
    )

    article = models.ForeignKey('Article', verbose_name=_('article'), on_delete=models.CASCADE,
                                related_name='comments')
    author = models.CharField(_('author'), max_length=100)
    email = models.EmailField(_('email'))
    url = models.URLField(_('url'), blank=True)
    body = models.TextField(_('body'))
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='n')
    created_time = models.DateTimeField(_('created time'), default=now)
    modified_time = models.DateTimeField(_('modified time'), default=now)
    parent_comment = models.ForeignKey('self', verbose_name=_('parent comment'), blank=True, null=True, on_delete=models.CASCADE,
                                        related_name='children')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), blank=True, null=True, on_delete=models.CASCADE,
                             related_name='comments')

    class Meta:
        ordering = ['created_time']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return self.body[:20]

    def save(self, *args, **kwargs):
        self.modified_time = now()
        super().save(*args, **kwargs)

    def get_admin_url(self):
        return reverse('admin:blog_comment_change', args=(self.id,))

    @property
    def author_name(self):
        if self.user:
            return self.user.username
        return self.author

    @property
    def created_time_format(self):
        return self.created_time.strftime('%Y-%m-%d %H:%M')