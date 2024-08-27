'''views'''
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Event

def home(request):
    '''Home page with all the events'''
    events = Event.objects.all()
    cities = Event.objects.values_list('city', flat=True).distinct()
    return render(request, 'home.html', {'events': events, 'cities': cities})

def event_detail(request, id):
    '''Event Detail page which returns the details of the event '''
    event = Event.objects.get(id=id)
    return render(request, 'event_detail.html', {'event': event})

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
