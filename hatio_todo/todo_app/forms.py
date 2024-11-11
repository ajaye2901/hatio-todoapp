from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UserRegisterForm(UserCreationForm) :
    email = forms.EmailField(required=True) 

    class Meta :
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title']

class ToDoForm(forms.ModelForm) :
    class Meta :
        model = ToDo
        fields = ['description'] 


