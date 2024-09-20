''' Creation and Updation of User and User Profile '''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    """ Customised User Creation Form to add EmailField """
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        """ Fields in User Form """
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        ''' Ensuring that email is unique for each user '''
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


# Form for UserProfile model fields
class UserProfileForm(forms.ModelForm):
    """ Customised User Profile """
    class Meta:
        """ Fields in User Profile """
        model = UserProfile
        fields = ['profile_picture', 'first_name', 'last_name', 'location']
