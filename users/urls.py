"""URLs"""

from django.urls import path, include
from . import views
from .views import home, signup

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/', signup, name="signup"),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path("events_by_city/", views.events_by_city, name="events_by_city"),
    path('events/<str:event_tag>/', views.events_by_tag, name='events_by_tag'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile_view, name='profile'),
]
