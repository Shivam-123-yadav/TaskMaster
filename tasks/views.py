from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Task, Comment
from projects.models import Project

@login_required
def task_create_view(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date') or None
        
        task = Task.objects.create(
            title=title,
            description=description,
            project=project,
            created_by=request.user,
            priority=priority,
            status=status,
            due_date=due_date
        )
        
        if assigned_to_id:
            task.assigned_to_id = assigned_to_id
            task.save()
        
        messages.success(request, 'Task created successfully!')
        return redirect('project_detail', pk=project.pk)
    
    context = {
        'project': project,
        'members': project.members.all()
    }
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all().select_related('user')
    
    context = {
        'task': task,
        'comments': comments,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def task_update_status(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        new_status = request.POST.get('status')
        task.status = new_status
        task.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'status': new_status})
        
        messages.success(request, 'Task status updated!')
        return redirect('task_detail', pk=pk)


@login_required
def comment_create_view(request, task_pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_pk)
        content = request.POST.get('content')
        
        Comment.objects.create(
            task=task,
            user=request.user,
            content=content
        )
        
        messages.success(request, 'Comment added!')
        return redirect('task_detail', pk=task_pk)
    

def some_view(request):
    notification_count = request.user.notifications.unread().count()  # adjust to your model
    return render(request, 'whatever.html', {'notification_count': notification_count})