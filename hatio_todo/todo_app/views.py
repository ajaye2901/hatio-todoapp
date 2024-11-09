from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

# Create your views here.

def register_view(request) :
    if request.method == 'POST' :
        form = UserRegisterForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('user_login')
    else :
        form = UserRegisterForm()
    
    return render(request, 'registration.html', {'form':form})

def user_login(request) :
    if request.method == 'POST' :
        form = AuthenticationForm(data=request.POST)
        if form.is_valid() :
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None :
                login(request, user)
                return redirect('home')
    else :
        form = AuthenticationForm()

    return render(request, 'login.html', {'form' : form})

def home(request) :
    return render(request, 'index.html')
    