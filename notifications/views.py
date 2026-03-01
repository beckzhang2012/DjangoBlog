from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic import ListView, FormView
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib import messages
from .models import Notification
from .forms import SystemNotificationForm
from .utils import send_system_notification
from accounts.models import BlogUser


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        queryset = self.request.user.notifications.all()
        
        # 筛选功能
        notification_type = self.request.GET.get('type')
        is_read = self.request.GET.get('is_read')
        search = self.request.GET.get('search')
        
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        if is_read is not None:
            queryset = queryset.filter(is_read=(is_read == 'true'))
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = self.request.user.notifications.filter(is_read=False).count()
        context['active_type'] = self.request.GET.get('type', 'all')
        context['search_query'] = self.request.GET.get('search', '')
        return context


@method_decorator(csrf_protect, name='dispatch')
class NotificationMarkAllReadView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return redirect('notifications:list')


@require_POST
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, recipient=request.user)
    notification.mark_as_read()
    return JsonResponse({'status': 'success'})


def get_unread_count(request):
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})


class SendSystemNotificationView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = SystemNotificationForm
    template_name = 'notifications/send_system_notification.html'
    success_url = '/notifications/'

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        recipient_choice = form.cleaned_data['recipient_choice']
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        url = form.cleaned_data['url']
        
        if recipient_choice == 'all':
            recipients = BlogUser.objects.filter(is_active=True)
        else:
            recipients = form.cleaned_data['recipients']
        
        send_system_notification(recipients, title, content, url)
        messages.success(self.request, _('系统通知已成功发送'))
        return super().form_valid(form)