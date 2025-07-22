from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Function to create a notification
def create_notification(user, message, notification_type='info'):
    Notification.objects.create(
        user=user,
        message=message,
        notification_type=notification_type,
        is_read=False
    )

# Create your views here.

# List notifications
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    # Mark all notifications as read when viewed
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

# Mark notification as read
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return HttpResponse('success')
