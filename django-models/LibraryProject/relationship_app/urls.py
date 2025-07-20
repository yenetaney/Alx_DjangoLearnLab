from django.urls import path
from . import views
from .views import list_books
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('library/details/<int:library_id>/', views.library_detail_view, name='library-detail-fbv'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail-cbv'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login'), name='logout'),
    path('register/', views.register, name='register'),
]
