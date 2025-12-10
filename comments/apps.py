from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'comments'
    
    def ready(self):
        # 加载审核dashboard
        import comments.dashboard
