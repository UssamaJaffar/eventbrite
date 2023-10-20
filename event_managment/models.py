from django.db import models

from user.models import User
# Create your models here.

class Venue(models.Model):
    Venue_id = models.IntegerField()
    User_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    is_deleted = models.BooleanField(default=False)
    address = models.CharField(max_length=1000)


class Event(models.Model):
    name = models.CharField(max_length=1000,default='')
    description = models.CharField(max_length=1000,default='')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    Event_id = models.IntegerField()
    Venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='venue')
    ticket_id = models.IntegerField(null=True)
    is_deleted = models.BooleanField(default=False)
