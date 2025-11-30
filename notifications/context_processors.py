from .models import Notification


def unread_notifications(request):
    if request.user.is_authenticated:
        return {
            'unread_notification_count': request.user.notifications.filter(is_read=0).count()
        }
    return {}