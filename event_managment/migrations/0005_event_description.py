# Generated by Django 4.2.6 on 2023-10-20 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_managment', '0004_event_end_time_event_name_event_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(default='', max_length=1000),
        ),
    ]