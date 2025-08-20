from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    user = request.user
    notifications = user.notifications.order_by('-timestamp')
    unread = notifications.filter(read=False)

    data = {
        'unread_count': unread.count(),
        'notifications': [
            {
                'actor': n.actor.username,
                'verb': n.verb,
                'target': str(n.target),
                'timestamp': n.timestamp,
                'read': n.read
            } for n in notifications
        ]
    }
    return Response(data)