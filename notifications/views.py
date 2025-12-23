from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Notification


@login_required
def notification_list(request):
    """通知列表"""
    notifications = request.user.notifications.all()
    
    # 筛选和搜索
    notification_type = request.GET.get('type')
    search_query = request.GET.get('search')
    
    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)
    
    if search_query:
        notifications = notifications.filter(
            models.Q(title__icontains=search_query) | 
            models.Q(content__icontains=search_query) |
            models.Q(sender__username__icontains=search_query)
        )
    
    # 分页
    paginator = Paginator(notifications, 20)
    page = request.GET.get('page')
    
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'selected_type': notification_type,
        'search_query': search_query
    })


@login_required
@require_POST
def mark_as_read(request, notification_id):
    """标记单条通知为已读"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.mark_as_read()
    return JsonResponse({'status': 'success'})


@login_required
@require_POST
def mark_all_as_read(request):
    """标记所有通知为已读"""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})


@login_required
def notification_detail(request, notification_id):
    """通知详情"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.mark_as_read()
    return render(request, 'notifications/notification_detail.html', {'notification': notification})


def get_unread_notifications_count(user):
    """获取未读通知数量"""
    if user.is_authenticated:
        return user.notifications.filter(is_read=False).count()
    return 0