from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserForm, UserProfileForm

# Create your views here.


from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm

class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

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
    
class HomeView(View):
    def get(self, request):
        return render(request, 'base.html')
