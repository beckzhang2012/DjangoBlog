from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'recipient', 'sender', 'notification_type', 
        'is_read', 'created_time'
    )
    list_filter = ('notification_type', 'is_read', 'created_time')
    search_fields = ('title', 'content', 'recipient__username', 'recipient__email')
    readonly_fields = ('created_time',)
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = _('标记为已读')

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = _('标记为未读')

    def has_add_permission(self, request):
        # 不允许在后台直接添加普通通知，系统通知通过专门的表单发送
        return request.user.is_superuser


admin.site.register(Notification, NotificationAdmin)