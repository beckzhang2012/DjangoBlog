from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Link(models.Model):
    name = models.CharField(_('name'), max_length=100)
    url = models.URLField(_('url'), default='https://example.com')
    description = models.TextField(_('description'), blank=True)
    index = models.IntegerField(_('index'), default=0, help_text=_('Enter a positive integer to set the order of the link. The smaller the number, the higher the priority.'))
    created_time = models.DateTimeField(_('created time'), default=now)
    modified_time = models.DateTimeField(_('modified time'), default=now)

    class Meta:
        ordering = ['index', 'created_time']
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified_time = now()
        super().save(*args, **kwargs)

    def get_admin_url(self):
        return reverse('admin:blog_link_change', args=(self.id,))


class Links(models.Model):
    name = models.CharField(_('name'), max_length=100)
    url = models.URLField(_('url'), default='https://example.com')
    description = models.TextField(_('description'), blank=True)
    index = models.IntegerField(_('index'), default=0, help_text=_('Enter a positive integer to set the order of the link. The smaller the number, the higher the priority.'))
    created_time = models.DateTimeField(_('created time'), default=now)
    modified_time = models.DateTimeField(_('modified time'), default=now)

    class Meta:
        ordering = ['index', 'created_time']
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified_time = now()
        super().save(*args, **kwargs)

    def get_admin_url(self):
        return reverse('admin:blog_links_change', args=(self.id,))