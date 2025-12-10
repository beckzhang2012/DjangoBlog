from .models import Notification


def notification_processor(request):
    """添加未读通知计数到上下文"""
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
    else:
        unread_count = 0
    
    return {
        'unread_notification_count': unread_count
    }