from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': Notification.objects.filter(
                recipient=request.user, 
                is_read=False
            ).count()
        }
    return {'unread_notifications_count': 0} 