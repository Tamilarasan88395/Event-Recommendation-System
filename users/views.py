""" views """

from collections import Counter
import random
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Event, UserProfile
from .forms import CustomUserCreationForm, UserProfileForm


def profile_view(request):
    """User Profile Updation"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid():
            user_form.username.save()  # This will save username and email
            return redirect("users:profile")
        if profile_form.is_valid():
            profile_form.save()  # This will save first & last name, profile_picture and location
            return redirect("users:profile")
    else:
        user_form = CustomUserCreationForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    return render(
        request,
        "profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "profile_picture": profile.profile_picture,
        },
    )


def recommend_events(user):
    """Generate a list of recommended events based on user activity."""
    # Get user profile
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        return Event.objects.none()  # Return empty queryset if no profile found

    # Parse search history and interaction data
    search_keywords = (
        user_profile.search_history.split(", ") if user_profile.search_history else []
    )
    interaction_keywords = (
        user_profile.interaction.split(", ") if user_profile.interaction else []
    )

    # Combine and count occurrences
    all_keywords = search_keywords + interaction_keywords
    keyword_counter = Counter(all_keywords)

    # Create a Q object to match any of the keywords
    q_objects = Q()
    for keyword in keyword_counter:
        q_objects |= Q(event_name__icontains=keyword) | Q(event_tag__icontains=keyword)

    # Query for events matching the user's preferences
    recommended_events = Event.objects.filter(q_objects).distinct()

    # Rank events based on keyword frequency
    ranked_events = sorted(
        recommended_events,
        key=lambda event: sum(
            keyword_counter.get(tag, 0) for tag in [event.event_name, event.event_tag]
        ),
        reverse=True,
    )

    top_ranked_events = random.sample(ranked_events, 5)

    return top_ranked_events


def home(request):
    """Home page with all the events"""
    # Retrieve all events and orders by date
    events = Event.objects.all().order_by("date")[:5]
    # Retrieve all unique event tags
    tags = Event.objects.values("event_tag")
    # Retrieve all unique city names
    cities = Event.objects.values_list("city", flat=True).distinct()

    tag_events = {}
    for tag in tags:
        tag_events[tag["event_tag"]] = Event.objects.filter(event_tag=tag["event_tag"])[:5]

    # Generate recommendations if the user is authenticated
    recommended_events = []
    if request.user.is_authenticated:
        recommended_events = recommend_events(request.user)

    return render(
        request,
        "home.html",
        {
            "events": events,
            "events_by_tag": tag_events,
            "cities": cities,
            "recommended_events": recommended_events,
        },
    )


def events_by_city(request):
    """Display events for a specific city"""

    # Get the city from the GET parameters
    selected_city = request.GET.get("city")

    if not selected_city:
        # Redirect to home if no city is selected
        return redirect("users:home")

    # Retrieve events for the selected city and ordering them by date
    events = Event.objects.filter(city=selected_city).order_by("date")

    # Set up pagination
    paginator = Paginator(events, 6)
    page_number = request.GET.get("page")
    events = paginator.get_page(page_number)

    return render(
        request,
        "events_by_city.html",
        {"events": events, "selected_city": selected_city},
    )


def event_detail(request, id):
    """Event Detail page which returns the details of the event"""
    event = Event.objects.get(id=id)

    # Store event interaction in UserActivity
    if request.user.is_authenticated:
        user_activity, created = UserProfile.objects.get_or_create(user=request.user)
        user_activity.interaction = (
            f"{user_activity.interaction}, {event.event_tag}"
            if user_activity.interaction
            else event.event_tag
        )
        user_activity.save()

    return render(request, "event_detail.html", {"event": event})


def events_by_tag(request, event_tag):
    """Display all events under a specific event_tag"""
    if event_tag == "Upcoming":
        events = Event.objects.all().order_by("date")
    else:
        events = Event.objects.filter(event_tag=event_tag).order_by("date")

    # Set up pagination
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

    events = Event.objects.filter(
        Q(event_name__icontains=query) | Q(event_tag__icontains=query)
    ).order_by("date")

    # Store search history in UserActivity
    if request.user.is_authenticated:
        user_activity, created = UserProfile.objects.get_or_create(user=request.user)
        user_activity.search_history = (
            f"{user_activity.search_history}, {query}"
            if user_activity.search_history
            else query
        )
        user_activity.save()

    paginator = Paginator(events, 6)
    page_number = request.GET.get("page")
    events = paginator.get_page(page_number)

    return render(request, "search_results.html", {"events": events, "query": query})


def signup(request):
    """Signup Page for User Registration"""

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
