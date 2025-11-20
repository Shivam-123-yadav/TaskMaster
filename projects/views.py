from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from tasks.models import Task

@login_required
def dashboard_view(request):
    user_projects = Project.objects.filter(members=request.user) | Project.objects.filter(owner=request.user)
    user_projects = user_projects.distinct()
    
    recent_tasks = Task.objects.filter(
        project__in=user_projects
    ).select_related('project', 'assigned_to')[:10]
    
    context = {
        'projects': user_projects[:5],
        'recent_tasks': recent_tasks,
        'total_projects': user_projects.count(),
        'total_tasks': Task.objects.filter(project__in=user_projects).count(),
        'completed_tasks': Task.objects.filter(project__in=user_projects, status='completed').count(),
    }
    return render(request, 'dashboard.html', context)


@login_required
def project_list_view(request):
    projects = Project.objects.filter(members=request.user) | Project.objects.filter(owner=request.user)
    projects = projects.distinct()
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.user != project.owner and request.user not in project.members.all():
        messages.error(request, 'You do not have access to this project')
        return redirect('project_list')
    
    tasks = project.tasks.all().select_related('assigned_to')
    
    context = {
        'project': project,
        'tasks': tasks,
        'todo_tasks': tasks.filter(status='todo'),
        'in_progress_tasks': tasks.filter(status='in_progress'),
        'review_tasks': tasks.filter(status='review'),
        'completed_tasks': tasks.filter(status='completed'),
    }
    return render(request, 'projects/project_detail.html', context)


@login_required
def project_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        start_date = request.POST.get('start_date') or None
        end_date = request.POST.get('end_date') or None
        
        project = Project.objects.create(
            name=name,
            description=description,
            status=status,
            owner=request.user,
            start_date=start_date,
            end_date=end_date
        )
        project.members.add(request.user)
        
        messages.success(request, 'Project created successfully!')
        return redirect('project_detail', pk=project.pk)
    
    return render(request, 'projects/project_form.html')