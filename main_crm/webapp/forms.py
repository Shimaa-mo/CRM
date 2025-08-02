from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput,TextInput
class CreateUserForm (UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']



class LoginForm(forms.Form):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=forms.PasswordInput)
