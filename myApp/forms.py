from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm
from django.contrib.auth.models import User

CITY_CHOICES = [
    ('Mekkah', 'Mekkah'),
    ('Buraydah', 'Buraydah'),
    ('Riyadh', 'Riyadh'),
    ('Jeddah', 'Jeddah'),
    ('Dammam', 'Dammam'),
]

class CustomerForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    
class Meta:
    model = User
    fields= ['username','email','password1','password2']

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class MyPasswordResetForm(PasswordChangeForm):
    pass
  
class ProfileForm(forms.ModelForm):
    city = forms.ChoiceField(choices=CITY_CHOICES)
    class Meta:
        model = UserProfile
        fields = ['city', 'mobile', 'zipcode']
    

