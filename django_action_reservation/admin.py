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
        'running_time',
        'state',
    )
    list_filter = (
        'action',
        'log__state',
    )

    @admin.display(ordering='log__started')
    def started(self, obj):
        return localize(localtime(obj.log.started)) if obj.log else None

    @admin.display(ordering='log__ended')
    def ended(self, obj):
        return localize(localtime(obj.log.ended)) if obj.log else None

    @admin.display()
    def running_time(self, obj):
        if obj.log:
            return (obj.log.ended - obj.log.started).seconds
        return None

    @admin.display(ordering='log__error_message')
    def error_message(self, obj):
        return obj.log.error_message if obj.log else None
    
    @admin.display(ordering='log__state')
    def state(self, obj):
        return obj.log.display_state if obj.log else None
