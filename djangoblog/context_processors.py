from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject

from notifications.models import Notification

def unread_notification_count(request):
    """Add unread notification count to the context for all users."""
    def get_count():
        if isinstance(request.user, AnonymousUser) or not request.user.is_authenticated:
            return 0
        return Notification.objects.filter(recipient=request.user, is_read=False).count()
    
    return {'unread_notification_count': SimpleLazyObject(get_count)}
