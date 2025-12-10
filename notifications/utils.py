from django.utils.translation import gettext_lazy as _
from .models import Notification, NotificationType


def send_comment_reply_notification(recipient, sender, comment, parent_comment):
    """发送评论回复通知"""
    title = _('您的评论收到了回复')
    content = _('用户 %(sender)s 回复了您的评论：%(reply_content)s') % {
        'sender': sender.username,
        'reply_content': comment.body[:50] + '...' if len(comment.body) > 50 else comment.body
    }
    url = f"{comment.article.get_absolute_url()}#div-comment-{comment.pk}"
    
    Notification.objects.create(
        recipient=recipient,
        sender=sender,
        title=title,
        content=content,
        notification_type=NotificationType.COMMENT_REPLY,
        url=url
    )


def send_system_notification(recipients, title, content, url=None):
    """发送系统通知，可以发送给单个用户或多个用户"""
    if not isinstance(recipients, list):
        recipients = [recipients]
    
    for recipient in recipients:
        Notification.objects.create(
            recipient=recipient,
            sender=None,
            title=title,
            content=content,
            notification_type=NotificationType.SYSTEM_NOTICE,
            url=url
        )


def send_article_review_notification(recipient, article, status):
    """发送文章审核通知"""
    if status == 'published':
        title = _('您的文章已通过审核')
        content = _('您的文章《%(title)s》已通过审核并发布。') % {'title': article.title}
    else:
        title = _('您的文章未通过审核')
        content = _('您的文章《%(title)s》未通过审核，请修改后重新提交。') % {'title': article.title}
    
    url = article.get_absolute_url() if status == 'published' else None
    
    Notification.objects.create(
        recipient=recipient,
        sender=None,
        title=title,
        content=content,
        notification_type=NotificationType.ARTICLE_REVIEW,
        url=url
    )