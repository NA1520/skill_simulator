from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('skill/<int:skill_id>/', views.skill_detail_view, name='skill_detail'),
    path('mission/<int:mission_id>/', views.mission_view, name='mission_detail'),
    path('profile/', views.profile_view, name='profile'),
]
