from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ProfileUpdateView
from . import views  # Your custom views (e.g., for registration)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
     path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]
