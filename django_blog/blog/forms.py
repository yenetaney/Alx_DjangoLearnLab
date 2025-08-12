from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from .models import Post
from .models import Comment



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content','tags',]  # author is not included as a form field

    def __init__(self, *args, **kwargs):
        # Optionally customize form initialization here
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Title cannot be empty.')
        # Add any other validation logic here
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only expose 'content' for input

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError("Comment cannot be empty.")
        return content