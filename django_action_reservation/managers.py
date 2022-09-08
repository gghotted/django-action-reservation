from django.db.models import Manager, QuerySet
from django.utils import timezone


class ReservationManager(Manager):
    def need_start(self):
        return self.get_queryset().filter(
            time__lt=timezone.now(),
            log=None,
        )


class TargetQuerySet(QuerySet):
    def reserve(self, action, time=None):
        time = time or timezone.now()
        reservation_model = self.model.reservation_model
        reservations = []
        for obj in self:
            reservation = reservation_model(
                action=action,
                time=time,
                target=obj,
            )
            reservations.append(reservation)
        return reservation_model.objects.bulk_create(reservations)


class TargetManager(Manager.from_queryset(TargetQuerySet)):
    ...


def target_reserve(self, action, time=None):
    time = time or timezone.now()
    return self.reservation_model.objects.create(action=action, time=time, target=self)
