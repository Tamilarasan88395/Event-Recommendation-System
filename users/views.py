'''views'''
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Event
from django.core.paginator import Paginator

from django.db.models import Count

def home(request):
    '''Home page with all the events'''
     # Retrieve all events and shuffe them
    events = Event.objects.all().order_by('?')[:5]
     # Retrieve all unique event tags
    tags = Event.objects.values('event_tag')

    events_by_tag = {}
    for tag in tags:
        events_by_tag[tag['event_tag']] = Event.objects.filter(event_tag=tag['event_tag'])[:5]
    
    return render(request, 'home.html', {'events': events, 'events_by_tag': events_by_tag})

def event_detail(request, id):
    '''Event Detail page which returns the details of the event '''
    event = Event.objects.get(id=id)
    return render(request, 'event_detail.html', {'event': event})

def events_by_tag(request, event_tag):
    '''Display all events under a specific event_tag'''
    if event_tag == 'Upcoming':
        events = Event.objects.all().order_by('?')
    else:
        events = Event.objects.filter(event_tag=event_tag)
    
    # Set up pagination (e.g., 5 events per page)
    paginator = Paginator(events, 6) 
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    
    return render(request, 'events_by_tag.html', {'events': events, 'event_tag': event_tag})

def search(request):
    '''Searching Event'''
    query = request.GET.get('q')
    if not query:
        return redirect('users:home')
    else:
        events = Event.objects.filter(event_name__icontains=query)
        return render(request, 'search_results.html', {'events': events, 'query': query})

def signup(request):
    '''Signup Page for User Registration'''
    
    class CustomUserCreationForm(UserCreationForm):
        email = forms.EmailField(required=True, max_length=254)

        class Meta:
            model = User
            fields = ("username", "email", "password1", "password2")
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = CustomUserCreationForm()
        form.fields['username'].help_text = ''
        form.fields['email'].help_text = ''
        form.fields['password1'].help_text = ''
        form.fields['password2'].help_text = ''
        if 'usable_password' in form.fields:
            del form.fields['usable_password']
    return render(request, 'registration/signup.html', {"form": form})
