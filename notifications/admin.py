from django.contrib import admin
from .models import Notification, NotificationType


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'title', 'is_read', 'creation_time', 'sender')
    list_filter = ('notification_type', 'is_read', 'creation_time')
    search_fields = ('recipient__username', 'title', 'content', 'sender__username')
    actions = ['mark_as_read', 'mark_as_unread']
    readonly_fields = ('creation_time', 'read_time')
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=1)
    mark_as_read.short_description = 'Mark selected notifications as read'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=0)
    mark_as_unread.short_description = 'Mark selected notifications as unread'


admin.site.register(Notification, NotificationAdmin)