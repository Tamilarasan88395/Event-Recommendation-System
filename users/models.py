"""Table Creation"""

import datetime
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    """ Event Details """

    event_tag = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(default=datetime.time(0, 0), null=True, blank=True)
    image_url = models.URLField(max_length=200)
    city = models.CharField(max_length=50)
    location = models.TextField()
    description = models.TextField(default="no description")
    booking_url = models.URLField(
        max_length=200,
        default=(
            "https://insider.in/event/u1s-long-drive-live-in-concert-coimbatore"
            "-oct12-2024/buy-page/shows/65cda8bb66eb4b000aaf16e9"
        ),
    )

    def __str__(self):
        """ returning the event_name """
        return str(self.event_name)

class UserProfile(models.Model):
    """ User Profile Details """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=10, blank=True, null=True)
    last_name = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        """ Handle image replacement or removal """
        try:
            old_profile = UserProfile.objects.get(id=self.id)
            if old_profile.profile_picture and old_profile.profile_picture != self.profile_picture:
                old_profile.profile_picture.delete(save=False)
        except UserProfile.DoesNotExist:
            pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ Delete the profile pricture if it exists """
        if self.profile_picture:
            self.profile_picture.delete(save=False)
        super().delete(*args, **kwargs)
    