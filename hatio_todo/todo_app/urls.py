from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('', user_login, name='login'),
    path('home/', home, name='home'),
    path('create_project/', create_project, name='create_project'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),  # Handles both viewing and creating todos
    path('todo/<int:todo_id>/update-status/', update_todo_status, name='update_todo_status'),
    path('todo/<int:todo_id>/delete/', delete_todo, name='delete_todo'),
    path('todo/<int:todo_id>/edit/', edit_todo, name='edit_todo'), 
    path('project/<int:project_id>/edit/', edit_project, name='edit_project'), 
    path('logout/', logout_view, name='logout'),
    path('project/<int:project_id>/export_gist/', export_project_gist, name='export_project_gist'),
]