from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    name = 'notifications'
    verbose_name = _('Notifications')
    
    def ready(self):
        # 导入信号
        import notifications.signals