from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
]