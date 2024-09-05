"""Admin Access for App and it's models"""

from django.contrib import admin
from .models import Event

admin.site.register(Event)
