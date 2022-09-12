# django-action-reservation

## Installation

Install using `pip`

```bash
pip install django-action-reservation
```

Add `'django-action-reservation'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = [
  	...
  	'django-action-reservation',
]
```

## Example

```python
# models.py

class PublishAction(Action):
    name = 'publish'

    def execute(self, post):
        post.is_published = True
        post.save()

        
class Post(models.Model):
    is_published = models.BooleanField(default=False)

    action_reservation = Reservation([PublishAction])

    
from django.utils.timezome import now
>> post = Post.objects.create()
>> post.reserve_action('publish', now())
>> Post.objects_for_reserve.all().reserve('publish')
```

## apis

### single reservation

model.reserve_action(action, time)

### bulk reservation

model.objects_for_reserve.all().reserve()

### model admin

`django_action_reservation.admin.ActionReservationAdmin`

```python
admin.site.register(models.Post.reservation_model, ActionReservationAdmin)
```

### inline reservation in admin

`django_action_reservation.admin.create_reservation_inline`

```python
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        create_reservation_inline(models.Post, extra=1),
    ]
```

### run threads

`django_action_reservation.reservation.Reservation.run_threads()`

```python
>> Reservation.run_threads()
or
bash >> python manage.py process_reservation
```

### settings

`ACTION_RESERVATION_CHECK_INTERVAL`: How often each thread confirms the reservation, default 10

`ACTION_RESERVATION_COOL_TIME`: Time to rest after performing the action, default 0

**in settings.py**

```python
ACTION_RESERVATION_CHECK_INTERVAL = 60
ACTION_RESERVATION_COOL_TIME = 10
```

**in action**

```python
class PublishAction(Action):
    check_interval = 60
    cool_time = 10
    name = 'publish'
```

