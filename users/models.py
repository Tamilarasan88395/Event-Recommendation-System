'''Table Ceation'''
import datetime
from django.db import models

class Event(models.Model):
    '''Event Details'''
    event_tag = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(default=datetime.time(0, 0), null=True, blank=True)
    image_url = models.URLField(max_length=200)
    city = models.CharField(max_length=50)
    location = models.TextField()
    description = models.TextField(default="no description")
    booking_url = models.URLField(max_length=200, default='https://insider.in/event/u1s-long-drive-live-in-concert-coimbatore-oct12-2024/buy-page/shows/65cda8bb66eb4b000aaf16e9')

    def __str__(self):
        '''returning the event_name to import_events.py'''
        return str(self.event_name)
