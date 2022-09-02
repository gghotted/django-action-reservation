from django.db import models
from django.utils.formats import localize
from django.utils.timezone import localtime

from django_action_reservation.managers import ReservationManager


class State:
    FAIL = 0
    SUCCESS = 1


class ActionLog(models.Model):
    started = models.DateTimeField(null=True)
    ended = models.DateTimeField(null=True)
    error_message = models.TextField()
    error_traceback = models.TextField()
    state = models.SmallIntegerField(choices=[
        (State.SUCCESS, 'success'),
        (State.FAIL, 'fail'),
    ])

    @property
    def display_state(self):
        return 'success' if self.state == State.SUCCESS else 'fail'


reservation_base_fields = {
    'created': models.DateTimeField(auto_now_add=True),
    'time': models.DateTimeField(),
    'log': models.OneToOneField(ActionLog, models.DO_NOTHING, null=True),
    'objects': ReservationManager(),
    '__str__': lambda self: '%s %s at %s' % (
        self.action,
        self.target,
        localize(localtime(self.time))
    )
}
