from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# Form for User model fields
class UserForm(forms.ModelForm):
    email = forms.EmailField(disabled=True)  # Email field is disabled

    class Meta:
        model = User
        fields = ['username', 'email']  # Only User fields

# Form for UserProfile model fields
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'first_name', 'last_name', 'location']  # Only UserProfile fields
