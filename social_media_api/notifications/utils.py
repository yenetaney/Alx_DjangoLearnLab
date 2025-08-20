from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, target):
    if recipient == actor:
        return  # Skip self-notifications

    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=ContentType.objects.get_for_model(target.__class__),
        object_id=target.id
    )