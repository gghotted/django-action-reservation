from django.db.models.signals import pre_delete
from django.dispatch import receiver

from django_action_reservation.models import ActionLog


@receiver(pre_delete)
def action_log_delete(sender, instance, **kwargs):
    if hasattr(instance, 'log') and isinstance(instance.log, ActionLog):
        instance.log.delete()
