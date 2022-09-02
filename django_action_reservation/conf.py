from appconf import AppConf
from django.conf import settings


class DjangoActionReservationAppConf(AppConf):
    CHECK_INTERVAL = 10
    COOL_TIME = 0

    class Meta:
        prefix = 'action_reservation'
