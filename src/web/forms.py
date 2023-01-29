from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField

from web.models import Post, Comment, User
from web.tasks import send_comment_notification

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email"}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class RegisterUserForm(CustomUserCreationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Password repeat"}))
    captcha = CaptchaField(label="")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "tags", "body", "status")


class CommentForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        request = self.initial["request"]
        post = self.initial["post"]
        link_to_post = request.build_absolute_uri(post.get_absolute_url())

        self.instance.author = self.initial["user"]
        self.instance.post = post
        self.instance.parent = self.initial["parent"]
        instance = super(CommentForm, self).save(*args, **kwargs)
        send_comment_notification.delay(instance.id, link_to_post)
        return instance

    class Meta:
        model = Comment
        fields = ("body",)


class ProfileUserChangeForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "user_profile_edit"}))
    vk_url = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "user_profile_edit"}))
    github_url = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "user_profile_edit"}))

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "bio",
            "profile_pic",
            "profile_background",
            "vk_url",
            "github_url",
        )


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "is_private",
        )
