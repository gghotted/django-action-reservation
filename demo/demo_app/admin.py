from django.contrib import admin
from django_action_reservation.admin import (ActionReservationAdmin,
                                             create_reservation_inline)

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        create_reservation_inline(models.Post, extra=1),
    ]


admin.site.register(models.Post.reservation_model, ActionReservationAdmin)
