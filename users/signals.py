''' Profile Management '''
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(instance, created):
    ''' Creation of User Profile for a new user '''

    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(instance):
    ''' Updation of User Profile ''' 

    instance.userprofile.save()
