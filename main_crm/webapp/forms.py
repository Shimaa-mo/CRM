from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput,TextInput
from .models import Record
class CreateUserForm (UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']



class LoginForm(forms.Form):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=forms.PasswordInput)


class CreateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['first_name','last_name','category', 'phone','tall','weight' ,'address']

class UpdateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['first_name','last_name','category', 'phone','tall','weight' ,'address']

