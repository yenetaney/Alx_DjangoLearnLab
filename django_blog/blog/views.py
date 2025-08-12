from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserForm, UserProfileForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, ProfileForm
from django import forms
from django.contrib.auth.models import User


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
    


