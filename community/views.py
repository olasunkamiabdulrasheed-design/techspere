from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Post, Comment
# Create your views here.


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'community/category_list.html', {'categories': categories})

def post_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.all().order_by('-created_at')
    return render(request, 'community/post_list.html', {'category': category, 'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            return redirect('post_detail', pk=post.pk)

    return render(request, 'community/post_detail.html', {'post': post, 'comments': comments})

@login_required
def post_create(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(category=category, author=request.user, title=title, content=content)
            return redirect('post_list', slug=category.slug)

    return render(request, 'community/post_create.html', {'category': category})