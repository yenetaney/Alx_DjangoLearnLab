from django.shortcuts import render
from .forms import BookSearchForm
from .forms import ExampleForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from .models import Book
# Create your views here.

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

class BookListView(PermissionRequiredMixin, ListView):
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.view_book'
    raise_exception = True
