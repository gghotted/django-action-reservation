from django.contrib import admin
from django.utils.formats import localize
from django.utils.timezone import localtime


def create_reservation_inline(model, base=admin.TabularInline, **kwargs):
    def get_queryset(self, request):
        return self.model.objects.need_start()

    res_model = model.reservation_model
    kwargs['model'] = res_model
    kwargs['verbose_name_plural'] = 'Need start reservations'
    kwargs['get_queryset'] = get_queryset
    kwargs['fields'] = (
        'time',
        'action',
    )
    return type(
        res_model.__name__ + base.__name__,
        (base, ),
        kwargs
    )


class ActionReservationAdmin(admin.ModelAdmin):
    fields = (
        'created',
        'target',
        'action',
        'time',
        'started',
        'ended',
        'error_message',
        'state',
    )
    readonly_fields = (
        'created',
        'started',
        'ended',
        'error_message',
        'state',
    )
    list_display = (
        'created',
        'id',
        'target',
        'action',
        'time',
        'started',
        'ended',
        'error_message',
        'state',
    )

    def started(self, obj):
        return localize(localtime(obj.log.started)) if obj.log else None

    def ended(self, obj):
        return localize(localtime(obj.log.ended)) if obj.log else None

    def error_message(self, obj):
        return obj.log.error_message if obj.log else None
    
    def state(self, obj):
        return obj.log.display_state if obj.log else None