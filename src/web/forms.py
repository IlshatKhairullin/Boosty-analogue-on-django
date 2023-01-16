from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

from web.models import Post, Comment, User

User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'tags', 'body', 'status')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class ProfileUserChangeForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'user_profile_edit'}))
    vk_url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'user_profile_edit'}))
    github_url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'user_profile_edit'}))

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'bio', 'profile_pic', 'profile_background', 'vk_url', 'github_url'
        )


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_private',)