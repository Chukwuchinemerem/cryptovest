from .models import SiteSettings


def site_settings(request):
    settings = SiteSettings.get_settings()
    unread_count = 0
    if request.user.is_authenticated:
        from notifications.models import Notification
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return {
        'site_settings': settings,
        'unread_notifications': unread_count,
    }
