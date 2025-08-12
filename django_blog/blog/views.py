from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserForm, UserProfileForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, ProfileForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm



# Create your views here.




class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class ProfileView(LoginRequiredMixin, View):

    def method(self, request):
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile')  # Redirect after successful update
        else:
            form = ProfileForm(instance=request.user)

        return render(request, 'profile_edit.html', {'form': form})

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
        return render(request, 'profile_edit.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect to profile page after successful update
        return render(request, 'profile_edit.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })
    
# Display all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'  # your template
    context_object_name = 'posts'
    ordering = ['-created_at']  # order newest first

# Show individual blog post details
class PostDetailView(DetailView):
    model = Post
    form_class = PostForm
    template_name = 'post_detail.html'

# Create a new post - only for authenticated users
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    fields = ['title', 'content']  # fields user can fill
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # set post author to current user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Update a post - only post author can update
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # allow only author

# Delete a post - only post author can delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
