from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from .models import Book

# Function-based view example:
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# OR Class-based view with permission and raise_exception:

class BookListView(PermissionRequiredMixin, ListView):
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.view_book'
    raise_exception = True
