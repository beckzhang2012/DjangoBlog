from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


# Create your models here.
class commands(models.Model):
    title = models.CharField('命令标题', max_length=300)
    command = models.CharField('命令', max_length=2000)
    describe = models.CharField('命令描述', max_length=300)
    creation_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '命令'
        verbose_name_plural = verbose_name


class EmailSendLog(models.Model):
    emailto = models.CharField('收件人', max_length=300)
    title = models.CharField('邮件标题', max_length=2000)
    content = models.TextField('邮件内容')
    send_result = models.BooleanField('结果', default=False)
    creation_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '邮件发送log'
        verbose_name_plural = verbose_name
        ordering = ['-creation_time']


class ReviewHistory(models.Model):
    """审核历史记录"""
    REVIEW_TYPE_CHOICES = (
        ('comment', _('Comment')),
        ('article', _('Article')),
    )
    
    REVIEW_RESULT_CHOICES = (
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('need_modification', _('Need Modification')),
    )
    
    # 审核相关信息
    review_type = models.CharField(
        _('review type'),
        max_length=10,
        choices=REVIEW_TYPE_CHOICES,
        blank=False,
        null=False
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('reviewer'),
        on_delete=models.CASCADE
    )
    review_time = models.DateTimeField(
        _('review time'),
        default=now,
        blank=False,
        null=False
    )
    result = models.CharField(
        _('review result'),
        max_length=20,
        choices=REVIEW_RESULT_CHOICES,
        blank=False,
        null=False
    )
    comment = models.TextField(
        _('review comment'),
        blank=True,
        null=True
    )
    
    # 关联被审核的内容（评论或文章）
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return f"{self.get_review_type_display()} review by {self.reviewer.username} on {self.review_time}"
    
    class Meta:
        ordering = ['-review_time']
        verbose_name = _('review history')
        verbose_name_plural = _('review histories')
