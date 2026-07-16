from django.urls import path
from . import views

urlpatterns = [
    path("resume-review/", views.resume_review, name="resume_review"),
    path("idea-generator/", views.idea_generator, name="idea_generator"),
    path("interview-prep/", views.interview_prep, name="interview_prep"),
]
