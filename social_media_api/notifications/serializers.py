from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source='actor.username')
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['actor', 'verb', 'target', 'timestamp', 'read']

    def get_target(self, obj):
        return str(obj.target)