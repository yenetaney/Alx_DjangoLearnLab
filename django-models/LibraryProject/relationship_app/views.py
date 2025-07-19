from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library, Book 
# Create your views here.

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()  # Access ManyToManyField
        return context
    
    def list_books_view(request):
        books = Book.objects.all()
        return render(request, 'relationship_app/list_books.html', {'books': books})
