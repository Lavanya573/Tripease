from notifications.models import Notification
from payment.models import Payment

def notification_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        # Only count payments that are not viewed
        recent_payments = Payment.objects.filter(user=request.user, is_viewed=False).count()
        return {
            'unread_notifications': unread_count,
            'recent_payments': recent_payments
        }
    return {
        'unread_notifications': 0,
        'recent_payments': 0
    } 