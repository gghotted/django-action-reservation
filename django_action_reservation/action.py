import threading
import traceback
from time import sleep

from django.utils import timezone

from django_action_reservation.conf import settings
from django_action_reservation.models import ActionLog, State


class Action:
    name = None
    cool_time = settings.ACTION_RESERVATION_COOL_TIME
    check_interval = settings.ACTION_RESERVATION_CHECK_INTERVAL

    def __init__(self, reservation_model):
        self.reservation_model = reservation_model

    def run_thread(self):
        t = threading.Thread(target=self.loop)
        t.daemon = True
        t.start()

    def reserve(self, target, time=None):
        time = time or timezone.now()
        self.reservation_model.objects.create(action=self.name, time=time, target=target)

    def loop(self):
        print('start thread %s (%s)' % (str(self.__class__), self.name))
        while True:
            reservations = self.reservation_model.objects.need_start().filter(
                action=self.name
            )
            for reservation in reservations:
                
                log = ActionLog()

                try:
                    log.started = timezone.now()
                    self.execute(reservation.target)
                    log.state = State.SUCCESS
                except Exception as e:
                    log.error_message = str(e)
                    log.error_traceback = traceback.format_exc()
                    log.state = State.FAIL
                log.ended = timezone.now()
                log.save()
                reservation.log = log
                reservation.save()
                sleep(self.cool_time)
            sleep(self.check_interval)

    def execute(self, obj):
        raise NotImplementedError
