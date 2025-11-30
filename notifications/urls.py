from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:notification_id>/mark_as_read/', views.mark_as_read, name='mark_as_read'),
    path('mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('send_system_notification/', views.send_system_notification, name='send_system_notification'),
]