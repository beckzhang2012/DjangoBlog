from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .models import Notification
from .forms import SystemNotificationForm


@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    
    # Filter by type
    notification_type = request.GET.get('type')
    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)
    
    # Search by content
    search_query = request.GET.get('search')
    if search_query:
        notifications = notifications.filter(content__icontains=search_query)
    
    # Count unread notifications
    unread_count = request.user.notifications.filter(is_read=0).count()
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'notification_type': notification_type,
        'search_query': search_query
    })


@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = 1
    notification.save()
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications:notification_list')


@login_required
def mark_all_as_read(request):
    request.user.notifications.filter(is_read=0).update(is_read=1)
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications:notification_list')


@permission_required('notifications.add_notification')
def send_system_notification(request):
    if request.method == 'POST':
        form = SystemNotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'System notification sent successfully')
            return redirect('admin:index')
    else:
        form = SystemNotificationForm()
    
    return render(request, 'notifications/send_system_notification.html', {'form': form})