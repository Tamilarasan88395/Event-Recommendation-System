""" views """

from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, User
from django.core.paginator import Paginator
from .models import Event


from .forms import UserProfileForm, UserForm
from .models import UserProfile

def profile_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # This will save first_name, last_name, and email
            profile_form.save()  # This will save profile_picture and location
            return redirect('users:profile')  # Redirect to a desired page after saving
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_picture': profile.profile_picture
    })

def home(request):
    """Home page with all the events"""
    # Retrieve all events and shuffe them
    events = Event.objects.all()[:5]
    # Retrieve all unique event tags
    tags = Event.objects.values("event_tag")
    # Retrieve all unique city names
    cities = Event.objects.values_list('city', flat=True).distinct()

    events_by_tag = {}
    for tag in tags:
        events_by_tag[tag["event_tag"]] = Event.objects.filter(
            event_tag=tag["event_tag"]
        )[:5]

    return render(
        request, "home.html", {"events": events, "events_by_tag": events_by_tag, "cities": cities}
    )

def events_by_city(request):
    """Display events for a specific city"""

    # Get the city from the GET parameters
    selected_city = request.GET.get('city')

    if not selected_city:
        # Redirect to home if no city is selected
        return redirect('home')

    # Retrieve events for the selected city
    events = Event.objects.filter(city=selected_city)

    return render(
        request, 'events_by_city.html', {
            'events': events,
            'selected_city': selected_city}
        )

def event_detail(request, id):
    """Event Detail page which returns the details of the event"""
    event = Event.objects.get(id=id)
    return render(request, "event_detail.html", {"event": event})


def events_by_tag(request, event_tag):
    """Display all events under a specific event_tag"""
    if event_tag == "Upcoming":
        events = Event.objects.all().order_by("?")
    else:
        events = Event.objects.filter(event_tag=event_tag)

    # Set up pagination (e.g., 5 events per page)
    paginator = Paginator(events, 6)
    page_number = request.GET.get("page")
    events = paginator.get_page(page_number)

    return render(
        request, "events_by_tag.html", {"events": events, "event_tag": event_tag}
    )


def search(request):
    """Searching Event"""
    query = request.GET.get("q")
    if not query:
        return redirect("users:home")
    else:
        events = Event.objects.filter(event_name__contains=query)
        return render(
            request, "search_results.html", {"events": events, "query": query}
        )


def signup(request):
    """Signup Page for User Registration"""

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
        form.fields["username"].help_text = ""
        form.fields["email"].help_text = ""
        form.fields["password1"].help_text = ""
        form.fields["password2"].help_text = ""
        if "usable_password" in form.fields:
            del form.fields["usable_password"]
    return render(request, "registration/signup.html", {"form": form})
