from django.db.models import Q
from django.utils import timezone
from django.http import HttpRequest
from main.models import Notification


def notifications(request:HttpRequest):
    user = request.user

    if not user.is_authenticated:
        messages = [{
            'message': notification.message,
            'read': True
        } for notification in Notification.objects.filter(visibility='public')]

        return {
            'notification': {
                'unread': 0,
                'messages': messages
            }
        }
    
    messages, unread = [], 0
    there_is_unread_notification = False
    notifications = Notification.objects.filter(
        Q(visibility__in=['public', 'memebers']) |
        Q(visibility='selected', users=user)
    ).distinct()
    
    for notification in notifications:
        read = user.is_authenticated and user.last_time_read_notifications > notification.notified_at

        if not read:
            unread += 1
            there_is_unread_notification = True

        messages.append({
            'message': notification.message,
            'read': read
        })

    if there_is_unread_notification and user.is_authenticated:
        user.last_time_read_notifications = timezone.now()
        user.save()
    
    return {
        'notification': {
            'unread': unread,
            'messages': messages
        }
    }