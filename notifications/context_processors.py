from .views import get_unread_notifications_count


def notification_processor(request):
    """上下文处理器：在模板中显示未读通知数量"""
    return {
        'unread_notifications_count': get_unread_notifications_count(request.user) if request.user.is_authenticated else 0
    }