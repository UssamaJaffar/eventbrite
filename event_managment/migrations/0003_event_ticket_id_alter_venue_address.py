# Generated by Django 4.2.6 on 2023-10-20 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_managment', '0002_venue_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ticket_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='address',
            field=models.CharField(max_length=1000),
        ),
    ]
