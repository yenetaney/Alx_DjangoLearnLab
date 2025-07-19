from django.urls import path
from . import views
from .views import list_books

urlpatterns = [
    path('library/details/<int:library_id>/', views.library_detail_view, name='library-detail-fbv'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail-cbv'),
]