from django.urls import path
from .views import (
    NotificationListView,
    NotificationMarkAllReadView,
    mark_as_read,
    get_unread_count,
    SendSystemNotificationView
)

app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name='list'),
    path('send-system-notification/', SendSystemNotificationView.as_view(), name='send_system_notification'),
    path('mark-all-read/', NotificationMarkAllReadView.as_view(), name='mark_all_read'),
    path('mark-as-read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    path('unread-count/', get_unread_count, name='unread_count'),
]