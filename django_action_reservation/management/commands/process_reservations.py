from time import sleep

from django.core.management.base import BaseCommand
from django_action_reservation.reservation import Reservation


class Command(BaseCommand):
    help = 'Process registered reservations'

    def handle(self, *args, **options):
        Reservation.run_threads()
        while True:
            sleep(42)
