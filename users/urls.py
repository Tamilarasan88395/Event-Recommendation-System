'''URLs'''
from . import views
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/', signup, name="signup"),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('search/', views.search, name='search'),
]
