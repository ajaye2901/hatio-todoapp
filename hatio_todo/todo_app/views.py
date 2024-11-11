from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import *
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import requests

# Create your views here.

def register_view(request) :
    if request.method == 'POST' :
        form = UserRegisterForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('login')
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

@login_required
def home(request):
    # Get all projects associated with the logged-in user
    projects = Project.objects.filter(user=request.user)
    return render(request, 'index.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)  # Save without committing to assign user
            project.user = request.user        # Set the logged-in user as the project owner
            project.save()                     # Save the project to the database
            return redirect('home')
    else:
        form = ProjectForm()

    # Get the list of user's projects to display on the index page
    user_projects = Project.objects.filter(user=request.user)
    return render(request, 'index.html', {'form': form, 'projects': user_projects})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    todos = project.todos.all()
    pending_todos = todos.filter(status='Pending')
    completed_todos = todos.filter(status='Completed')
    
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.project = project
            todo.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ToDoForm()

    return render(request, 'project_detail.html', {
        'project': project,
        'pending_todos': pending_todos,
        'completed_todos': completed_todos,
        'total_todos_count': todos.count(),
        'completed_todos_count': completed_todos.count(),
        'form': form,
    })

# New view to handle the update of todo status
def update_todo_status(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)
    
    # Toggle the status of the todo item
    if todo.status == 'Pending':
        todo.status = 'Completed'
    else:
        todo.status = 'Pending'
    
    todo.save()
    
    # Redirect back to the project details page
    return redirect('project_detail', project_id=todo.project.id)


def delete_todo(request, todo_id):
    # Fetch the todo object using the todo_id
    todo = get_object_or_404(ToDo, id=todo_id)

    if request.method == 'POST':
        todo.delete()  # Delete the todo
        return redirect('project_detail', project_id=todo.project.id)  # Redirect back to the project details page

    return redirect('project_detail', project_id=todo.project.id)


@login_required
def edit_todo(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, project__user=request.user)  # Ensure the todo belongs to the logged-in user
    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=todo.project.id)  # Redirect to the project detail page
    else:
        form = ToDoForm(instance=todo)  # Prepopulate the form with existing todo data

    return render(request, 'edit_todo.html', {
        'form': form,
        'todo': todo,
    })

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)  # Ensure the project belongs to the logged-in user
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect back to the home page (or wherever you need)
    else:
        form = ProjectForm(instance=project)  # Prepopulate the form with current project details

    return render(request, 'edit_project.html', {
        'form': form,
        'project': project,
    })

def logout_view(request):
    logout(request)
    return redirect('login')

def export_project_gist(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    todos = project.todos.all()
    
    # Count completed and total todos
    total_todos = todos.count()
    completed_todos = todos.filter(status='Completed').count()
    pending_todos = todos.filter(status='Pending')

    # Prepare content for markdown file
    markdown_content = f"# {project.title}\n\n"
    markdown_content += f"**Summary**: {completed_todos} / {total_todos} completed.\n\n"
    
    # Section 1: Pending Todos
    markdown_content += "## Pending Todos\n"
    for todo in pending_todos:
        markdown_content += f"- [ ] {todo.description}\n"
    
    # Section 2: Completed Todos
    markdown_content += "\n## Completed Todos\n"
    for todo in todos.filter(status='Completed'):
        markdown_content += f"- [x] {todo.description}\n"
    
    # Define the file name and path
    file_name = f"{project.title.replace(' ', '_')}.md"  # Project title without spaces
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # Save the markdown content to the file
    with open(file_path, 'w') as file:
        file.write(markdown_content)

    # Optionally, return the file as a response to the user for download
    response = HttpResponse(content=markdown_content, content_type='text/markdown')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response