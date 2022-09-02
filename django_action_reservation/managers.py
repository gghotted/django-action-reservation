from django.db.models import Manager
from django.utils import timezone


class ReservationManager(Manager):
    def need_start(self):
        return self.get_queryset().filter(
            time__lt=timezone.now(),
            log=None,
        )
