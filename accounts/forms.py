from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'skills', 'experience_level', 'github_link', 'linkedin_link', 'portfolio_link', 'profile_photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell people a bit about yourself...'}),
            'skills': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, React'}),
            'github_link': forms.URLInput(attrs={'placeholder': 'https://github.com/yourusername'}),
            'linkedin_link': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourusername'}),
            'portfolio_link': forms.URLInput(attrs={'placeholder': 'https://yourportfolio.com'}),
        }