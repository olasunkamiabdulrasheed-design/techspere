from django.shortcuts import render
from community.models import Post
from teams.models import Project
from accounts.models import CustomUser

def search_view(request):
    query = request.GET.get('q', '')
    posts = []
    projects = []
    users = []

    if query:
        posts = Post.objects.filter(title__icontains=query).order_by('-created_at')
        projects = Project.objects.filter(title__icontains=query).order_by('-created_at')
        users = CustomUser.objects.filter(username__icontains=query)

    return render(request, 'search/results.html', {
        'query': query,
        'posts': posts,
        'projects': projects,
        'users': users,
    })