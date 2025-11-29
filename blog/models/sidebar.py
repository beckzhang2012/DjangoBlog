from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class SideBar(models.Model):
    TYPE_CHOICES = (
        ('h', _('HTML')),
        ('t', _('Text')),
        ('r', _('Recent Articles')),
        ('a', _('Archive')),
        ('c', _('Categories')),
        ('t', _('Tags')),
    )

    name = models.CharField(_('name'), max_length=100)
    content = models.TextField(_('content'), blank=True, help_text=_('If type is HTML or Text, enter the content here.'))
    type = models.CharField(_('type'), max_length=1, choices=TYPE_CHOICES, default='t')
    sequence = models.IntegerField(_('sequence'), default=0, help_text=_('Enter a positive integer to set the order of the sidebar. The smaller the number, the higher the priority.'))
    is_enabled = models.BooleanField(_('is enabled'), default=True)
    created_time = models.DateTimeField(_('created time'), default=now)
    modified_time = models.DateTimeField(_('modified time'), default=now)

    class Meta:
        ordering = ['sequence', 'created_time']
        verbose_name = _('sidebar')
        verbose_name_plural = _('sidebars')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified_time = now()
        super().save(*args, **kwargs)

    def get_admin_url(self):
        return reverse('admin:blog_sidebar_change', args=(self.id,))