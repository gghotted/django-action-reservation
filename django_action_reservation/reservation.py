import importlib

from django.db import models

from django_action_reservation.models import reservation_base_fields


class Reservation:
    instances = []

    def __init__(self, action_classes):
        self.check_names(action_classes)
        self.action_classes = action_classes
        self.actions = []
        self.instances.append(self)

    def contribute_to_class(self, cls, name):
        res_model = self.create_reservation_model(cls)
        module = importlib.import_module(cls.__module__)
        setattr(module, res_model.__name__, res_model)
        cls.reservation_model = res_model

        self.actions.extend([c(cls.reservation_model) for c in self.action_classes])

    def create_reservation_model(self, cls):
        name = cls.__name__ + 'ActionReservation'
        bases = (models.Model, )
        attrs = {
            **reservation_base_fields,
            'action': self.create_action_field(),
            'target': models.ForeignKey(
                cls,
                models.DO_NOTHING,
                related_name='reservations',
            ),
            '__module__': cls.__module__
        }
        return type(name, bases, attrs)

    def create_action_field(self):
        return models.CharField(
            max_length=255,
            choices=[
                (name, name)
                for name in self.action_names
            ]
        )

    def check_names(self, action_classes):
        name_list = [c.name for c in action_classes]
        name_set = {c.name for c in action_classes}
        if len(name_list) != len(name_set):
            raise Exception('action names must unique')

    @property
    def action_names(self):
        return [a.name for a in self.action_classes]

    @classmethod
    def run_threads(cls):
        for instance in cls.instances:
            for action in instance.actions:
                action.run_thread()
