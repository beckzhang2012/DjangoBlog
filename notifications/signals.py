from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags
from .models import Notification
from comments.models import Comment


@receiver(post_save, sender=Comment)
def send_comment_reply_notification(sender, instance, created, **kwargs):
    """当有评论回复时发送通知"""
    if created and instance.parent_comment and instance.parent_comment.author != instance.author:
        # 发送评论回复通知
        recipient = instance.parent_comment.author
        sender_user = instance.author
        article = instance.article
        
        # 创建通知内容
        title = f"您的评论有新回复"
        content = f"{sender_user.username} 回复了您的评论：{strip_tags(instance.body)}"
        target_url = reverse('blog:detailbyid', kwargs={
            'article_id': article.id,
            'year': article.creation_time.year,
            'month': article.creation_time.month,
            'day': article.creation_time.day
        })
        
        # 创建通知
        Notification.objects.create(
            recipient=recipient,
            sender=sender_user,
            title=title,
            content=content,
            notification_type='comment_reply',
            target_url=target_url
        )


# 可以添加更多信号处理器，比如文章审核通知等