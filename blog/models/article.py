from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from uuslug import slugify

from djangoblog.utils import cache_decorator, cache


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('p', _('Published')),
    )

    COMMENT_STATUS = (
        ('o', _('Open')),
        ('c', _('Closed')),
    )

    TYPE = (
        ('a', _('Article')),
        ('p', _('Page')),
    )

    title = models.CharField(_('title'), max_length=200, unique=True)
    body = models.TextField(_('body'))
    excerpt = models.TextField(_('excerpt'), blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'), on_delete=models.CASCADE)
    category = models.ForeignKey('Category', verbose_name=_('category'), on_delete=models.CASCADE,
                                 related_name='article_category')
    tags = models.ManyToManyField('Tag', verbose_name=_('tags'), blank=True, related_name='article_tag')
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='p')
    comment_status = models.CharField(_('comment status'), max_length=1, choices=COMMENT_STATUS,
                                      default='o')
    type = models.CharField(_('type'), max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField(_('views'), default=0)
    created_time = models.DateTimeField(_('created time'), default=now)
    modified_time = models.DateTimeField(_('modified time'), default=now)
    article_order = models.IntegerField(_('article order'), default=0, help_text=_('Enter a positive integer to set the order of the article. The smaller the number, the higher the priority.'))
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        get_latest_by = 'created_time'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.modified_time = now()
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # 集成版本管理功能
        from .article_version import ArticleVersion
        ArticleVersion.create_version(self, self.author)

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})

    @cache_decorator(60 * 10)
    def next_article(self):
        # 下一篇
        return Article.objects.filter(id__gt=self.id, status='p').order_by('id').first()

    @cache_decorator(60 * 10)
    def prev_article(self):
        # 上一篇
        return Article.objects.filter(id__lt=self.id, status='p').order_by('-id').first()

    def viewed(self):
        # 增加阅读量
        self.views += 1
        self.save(update_fields=['views'])

    def get_admin_url(self):
        return reverse('admin:blog_article_change', args=(self.id,))

    @property
    def category_name(self):
        return self.category.name

    @property
    def tag_names(self):
        return [tag.name for tag in self.tags.all()]

    @property
    def author_name(self):
        return self.author.username

    @property
    def created_time_format(self):
        return self.created_time.strftime('%Y-%m-%d %H:%M')

    @property
    def modified_time_format(self):
        return self.modified_time.strftime('%Y-%m-%d %H:%M')


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True)
    parent_category = models.ForeignKey('self', verbose_name=_('parent category'), blank=True, null=True, on_delete=models.CASCADE,
                                        related_name='children')
    index = models.IntegerField(_('index'), default=0, help_text=_('Enter a positive integer to set the order of the category. The smaller the number, the higher the priority.'))
    created_time = models.DateTimeField(_('created time'), default=now)
    modified_time = models.DateTimeField(_('modified time'), default=now)

    class Meta:
        ordering = ['index', 'created_time']
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        unique_together = ('name', 'parent_category')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified_time = now()
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return reverse('admin:blog_category_change', args=(self.id,))


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True)
    created_time = models.DateTimeField(_('created time'), default=now)
    modified_time = models.DateTimeField(_('modified time'), default=now)

    class Meta:
        ordering = ['created_time']
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified_time = now()
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return reverse('admin:blog_tag_change', args=(self.id,))