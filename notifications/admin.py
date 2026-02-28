from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'sender', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'content', 'recipient__username', 'sender__username')
    readonly_fields = ('created_at',)
    
    def has_add_permission(self, request):
        # 管理员可以通过管理后台发送系统通知
        return request.user.is_superuser
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # 如果是添加新通知，默认设置为系统通知
        if obj is None:
            form.base_fields['notification_type'].initial = 'system_notice'
        return form