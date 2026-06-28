from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('new/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/apply/', views.join_request_create, name='join_request_create'),
    path('request/<int:pk>/<str:action>/', views.manage_join_request, name='manage_join_request'),
]