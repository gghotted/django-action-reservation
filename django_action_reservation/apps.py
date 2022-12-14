import sys

from django.apps import AppConfig


class DjangoActionReservationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_action_reservation'

    def ready(self):
        from django_action_reservation import signals
