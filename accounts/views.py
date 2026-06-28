from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from .models import CustomUser
# Create your views here.


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', username=user.username)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def profile_view(request, username):
    user = CustomUser.objects.get(username=username)
    return render(request, 'accounts/profile.html', {'profile_user': user})