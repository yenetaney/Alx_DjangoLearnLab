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
     path('admin-area/', views.admin_view, name='admin_view'),
    path('librarian-area/', views.librarian_view, name='librarian_view'),
    path('member-area/', views.member_view, name='member_view'),
     path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]


