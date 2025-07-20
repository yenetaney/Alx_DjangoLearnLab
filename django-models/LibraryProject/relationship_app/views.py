from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library, Book 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

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

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            return redirect('home')  # Change 'home' to your desired redirect
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def check_role(role):
    def role_check(user):
        return hasattr(user, 'userprofile') and user.userprofile.role == role
    return user_passes_test(role_check)

@check_role('Admin')
def admin_view(request):
    return render(request, 'admin_view.html')

@check_role('Librarian')
def librarian_view(request):
    return render(request, 'librarian_view.html')

@check_role('Member')
def member_view(request):
    return render(request, 'member_view.html')
