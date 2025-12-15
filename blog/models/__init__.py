from django.utils.translation import gettext_lazy as _
from django.db import models

class LinkShowType(models.TextChoices):
    L = 'L', _('Link')
    I = 'I', _('Image')
    A = 'A', _('All')

from .article import Article, Category, Tag
from .article_version import ArticleVersion
from .comment import Comment
from .link import Link, Links
from .sidebar import SideBar
from .settings import BlogSettings