from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from community.models import Post
from teams.models import Project, JoinRequest

def home_view(request):
    return render(request, 'core/home.html')

@login_required
def dashboard_view(request):
    recent_posts = Post.objects.all().order_by('-created_at')[:10]
    recent_projects = Project.objects.all().order_by('-created_at')[:6]
    my_projects = Project.objects.filter(creator=request.user)
    my_applications = JoinRequest.objects.filter(applicant=request.user).select_related('project')

    return render(request, 'core/dashboard.html', {
        'recent_posts': recent_posts,
        'recent_projects': recent_projects,
        'my_projects': my_projects,
        'my_applications': my_applications,
    })