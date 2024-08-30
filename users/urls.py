'''URLs'''
from . import views
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/', signup, name="signup"),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('events/<str:event_tag>/', views.events_by_tag, name='events_by_tag'),
    path('search/', views.search, name='search'),
]
