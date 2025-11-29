from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class BlogSettings(models.Model):
    site_name = models.CharField(_('site name'), max_length=100)
    site_description = models.CharField(_('site description'), max_length=200)
    site_keywords = models.CharField(_('site keywords'), max_length=200)
    site_url = models.URLField(_('site url'), default='https://example.com')
    site_logo = models.ImageField(_('site logo'), upload_to='blog/logos/', blank=True)
    site_favicon = models.ImageField(_('site favicon'), upload_to='blog/favicons/', blank=True)
    site_analytics = models.TextField(_('site analytics'), blank=True, help_text=_('Enter your analytics code here.'))
    site_copyright = models.TextField(_('site copyright'), blank=True)
    created_time = models.DateTimeField(_('created time'), default=now)
    modified_time = models.DateTimeField(_('modified time'), default=now)

    class Meta:
        verbose_name = _('blog setting')
        verbose_name_plural = _('blog settings')

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.modified_time = now()
        super().save(*args, **kwargs)

    def get_admin_url(self):
        return reverse('admin:blog_blogsettings_change', args=(self.id,))