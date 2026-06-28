from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, JoinRequest

def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'teams/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = JoinRequest.objects.filter(project=project, applicant=request.user).exists()
    return render(request, 'teams/project_detail.html', {'project': project, 'already_applied': already_applied})

@login_required
def project_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        roles_needed = request.POST.get('roles_needed')
        if title and description:
            Project.objects.create(
                creator=request.user,
                title=title,
                description=description,
                roles_needed=roles_needed
            )
            return redirect('project_list')
    return render(request, 'teams/project_create.html')

@login_required
def join_request_create(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        message = request.POST.get('message')
        JoinRequest.objects.get_or_create(project=project, applicant=request.user, defaults={'message': message})
    return redirect('project_detail', pk=project.pk)



@login_required
def manage_join_request(request, pk, action):
    join_request = get_object_or_404(JoinRequest, pk=pk)

    # Only the project creator can accept/reject
    if request.user != join_request.project.creator:
        return redirect('project_detail', pk=join_request.project.pk)

    if action == 'accept':
        join_request.status = 'accepted'
    elif action == 'reject':
        join_request.status = 'rejected'
    join_request.save()

    return redirect('project_detail', pk=join_request.project.pk)