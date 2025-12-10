from django.urls import path
from django.urls import re_path

from . import views
from .forms import LoginForm

app_name = "accounts"

urlpatterns = [re_path(r'^login/$',
                       views.LoginView.as_view(success_url='/'),
                       name='login',
                       kwargs={'authentication_form': LoginForm}),
               re_path(r'^register/$',
                       views.RegisterView.as_view(success_url="/"),
                       name='register'),
               re_path(r'^logout/$',
                       views.LogoutView.as_view(),
                       name='logout'),
               path(r'account/result.html',
                    views.account_result,
                    name='result'),
               re_path(r'^forget_password/$',
                       views.ForgetPasswordView.as_view(),
                       name='forget_password'),
               re_path(r'^forget_password_code/$',
                       views.ForgetPasswordEmailCode.as_view(),
                       name='forget_password_code'),
               # 通知相关路由
               re_path(r'^notifications/$',
                       views.NotificationListView.as_view(),
                       name='notifications'),
               re_path(r'^notifications/(?P<notification_id>\d+)/mark_as_read/$',
                       views.NotificationMarkAsReadView.as_view(),
                       name='notification_mark_as_read'),
               re_path(r'^notifications/mark_all_as_read/$',
                       views.NotificationMarkAllAsReadView.as_view(),
                       name='notification_mark_all_as_read'),
               ]
