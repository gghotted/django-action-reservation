from django.db import models
from django_action_reservation.action import Action
from django_action_reservation.reservation import Reservation


class PublishAction(Action):
    name = 'publish'

    def execute(self, post):
        post.is_published = True
        post.save()


class RaiseErrorAction(Action):
    name = 'raise error'

    def execute(self, post):
        raise Exception('some problem in %s' % str(post))


class CoolTime10(Action):
    name = 'cooltime 10 sec'
    cool_time = 10

    def execute(self, post):
        pass


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    action_reservation = Reservation([PublishAction, RaiseErrorAction, CoolTime10])
