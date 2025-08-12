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
from .models import Post, Comment
from .forms import CommentForm
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q


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
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # or wherever you want to redirect

        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
        else:
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)

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

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return self.post.get_absolute_url()
    
class PostSearchView(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)  # for django-taggit
            ).distinct()
        return Post.objects.none()
    
class PostsByTagView(ListView):
    model = Post
    template_name = 'posts_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        return Post.objects.filter(tags__name=tag_name)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs['tag_name']
        return context