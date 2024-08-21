'''views'''
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

def home(request):
    ''' returning the home page '''
    return render(request, 'home.html', {})


def signup(request):
    '''returning the signup page'''
    
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
        form.fields['password1'].help_text = ''
        form.fields['password2'].help_text = ''
        if 'usable_password' in form.fields:
            del form.fields['usable_password']
    return render(request, 'registration/signup.html', {"form": form})
