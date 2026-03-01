import difflib
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class ArticleVersion(models.Model):
    """文章版本模型"""
    article = models.ForeignKey(
        'blog.Article',
        verbose_name=_('article'),
        on_delete=models.CASCADE,
        related_name='versions'
    )
    version_number = models.PositiveIntegerField(_('version number'), default=1)
    title = models.CharField(_('title'), max_length=200)
    body = models.TextField(_('body'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(_('created at'), default=now)
    is_active = models.BooleanField(_('is active'), default=False)

    class Meta:
        ordering = ['-version_number']
        verbose_name = _('article version')
        verbose_name_plural = _('article versions')

    def __str__(self):
        return f"{self.article.title} - Version {self.version_number}"

    @staticmethod
    def create_version(article, user):
        """创建新的文章版本"""
        # 获取当前最新版本号
        latest_version = article.versions.order_by('-version_number').first()
        version_number = latest_version.version_number + 1 if latest_version else 1

        # 创建新版本
        return ArticleVersion.objects.create(
            article=article,
            version_number=version_number,
            title=article.title,
            body=article.body,
            author=user,
            is_active=False
        )

    def compare_with(self, other_version):
        """与另一个版本比较差异"""
        if not isinstance(other_version, ArticleVersion):
            raise ValueError("必须提供一个ArticleVersion实例")

        # 比较标题
        title_diff = []
        if self.title != other_version.title:
            title_diff = list(difflib.ndiff([other_version.title], [self.title]))

        # 比较正文
        body_diff = list(difflib.ndiff(other_version.body.splitlines(), self.body.splitlines()))

        return {
            'title_diff': title_diff,
            'body_diff': body_diff
        }

    def restore(self, user):
        """恢复到这个版本，会创建一个新的版本"""
        # 更新当前文章内容
        self.article.title = self.title
        self.article.body = self.body
        self.article.save()

        # 创建新的版本记录
        new_version = ArticleVersion.objects.create(
            article=self.article,
            version_number=self.article.versions.count() + 1,
            title=self.title,
            body=self.body,
            author=user,
            is_active=True
        )

        # 标记其他版本为非活跃
        ArticleVersion.objects.filter(article=self.article).exclude(id=new_version.id).update(is_active=False)

        return new_version