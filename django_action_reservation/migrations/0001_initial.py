# Generated by Django 4.1 on 2022-09-02 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateTimeField(null=True)),
                ('ended', models.DateTimeField(null=True)),
                ('error_message', models.TextField()),
                ('error_traceback', models.TextField()),
                ('state', models.SmallIntegerField(choices=[(1, 'success'), (0, 'fail')])),
            ],
        ),
    ]