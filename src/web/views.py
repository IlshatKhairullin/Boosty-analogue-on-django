from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q, Count
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterUserForm, PostForm, CommentForm, ProfileUserChangeForm, ProfileSettingsForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from .models import *


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("post_list")
    else:
        form = AuthenticationForm()
    return render(request, "account/login.html", {form: form})


class Register(View):
    template_name = "registration/register.html"

    def get(self, request):
        context = {"form": RegisterUserForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            human = True
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect("/home")

        context = {"form": form}
        return render(request, self.template_name, context)


class AuthorProfile(DetailView):
    model = User
    template_name = "web/profile_look_for_other_users.html"
    slug_field = "id"
    slug_url_kwarg = "id"


class LikedPostsListView(ListView):
    template_name = "web/profile_liked_posts.html"
    context_object_name = "liked_posts"
    paginate_by = 40

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        queryset = user.post_like.all()
        return queryset


class PostListView(ListView):
    template_name = "web/main_page.html"
    context_object_name = "posts"
    paginate_by = 20
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_queryset(self):
        queryset = Post.objects.filter(status=Status.published)

        if "popularity_post" in self.request.GET:
            queryset = queryset.annotate(total_views=Count("views", distinct=True)).order_by("-total_views")
        elif "rating_post" in self.request.GET:
            queryset = queryset.annotate(total_likes=Count("likes", distinct=True)).order_by("-total_likes")

        return self.filter_queryset(queryset)

    def filter_queryset(self, posts):
        self.search = self.request.GET.get("search", None)

        if self.search:
            # Q - спец объект, у которого определены логические операции (и, или...)
            posts = posts.filter(Q(title__icontains=self.search) | Q(body__icontains=self.search))
        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        filtered_posts = Post.objects.filter(status=Status.published)

        return {
            **super(PostListView, self).get_context_data(**kwargs),
            "most_popular_tags": Post.tags.most_common(extra_filters={"post__in": filtered_posts})[:4],
            "search": self.request.GET.get("search"),
        }


@login_required(login_url="/login/")
def LikePostView(request, post_slug, post_id):
    if "post_like_post_detail" in request.POST:
        post = get_object_or_404(Post, id=request.POST.get("post_like_post_detail"))
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect("post_detail", slug=post_slug, id=post_id)

    if "post_like_main_page":
        post = get_object_or_404(Post, id=request.POST.get("post_like_main_page"))
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect("post_list")


@login_required(login_url="/login/")
def LikeCommentView(request, post_slug, post_id, comment_id):
    if "comment_like" in request.POST:
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return redirect("post_detail", slug=post_slug, id=post_id)


class TagIndexView(ListView):
    model = Post
    template_name = "web/main_page.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get("tag_slug"))

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            **super(TagIndexView, self).get_context_data(**kwargs),
            "most_popular_tags": Post.tags.most_common()[:4],
        }


class DetailPostView(SuccessMessageMixin, FormMixin, DetailView):
    # FormMixin - тк изначально в DetailView нет параметра form_class
    model = Post
    form_class = CommentForm
    success_message = "Комментарий успешно добавлен"
    template_name = "web/post_detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.parent_obj = None

        try:  # проверка на тот случай, если к нам прилетел не тот parent_id откуда то еще
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                self.parent_obj = parent_qs.first()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user = None if self.request.user.is_anonymous else self.request.user
        self.object = CommentForm(
            data=self.request.POST,
            initial={"user": user, "post": self.get_object(), "parent": self.parent_obj, "request": self.request},
        )
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs["id"])
        total_post_likes = post.number_of_likes()
        total_views = post.number_of_views()

        if self.request.user.is_authenticated:
            post.views.add(self.request.user)

        post_liked = False
        if post.likes.filter(id=self.request.user.id):
            post_liked = True

        return {
            **super(DetailPostView, self).get_context_data(**kwargs),
            "total_post_likes": total_post_likes,
            "post_liked": post_liked,
            "post_views": total_views,
        }

    def get_success_url(self, **kwargs):
        return reverse("post_detail", args=(self.kwargs["slug"], self.kwargs[self.slug_url_kwarg]))


class UpdateCommentView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "web/comment_detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        return {
            **super(UpdateCommentView, self).get_context_data(**kwargs),
            "slug": self.kwargs["slug"],
            "post_id": self.kwargs["post_id"],
        }

    def get_success_url(self, **kwargs):
        return reverse("post_detail", args=(self.kwargs["slug"], self.kwargs["post_id"]))


class DeleteCommentView(DeleteView):
    model = Comment
    slug_field = "id"
    slug_url_kwarg = "id"

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse("post_detail", args=(self.kwargs["slug"], self.kwargs["post_id"]))


class DetailPostEditView(DetailView):
    model = Post
    template_name = "web/post_edit_detail.html"
    context_object_name = "post"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        return {**super(DetailPostEditView, self).get_context_data(**kwargs), "id": self.kwargs[self.slug_url_kwarg]}


class PostCreateView(CreateView):
    template_name = "web/post_add_edit_form.html"
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile_user_posts")


class PostUpdateView(UpdateView):
    template_name = "web/post_add_edit_form.html"
    form_class = PostForm
    slug_field = "id"
    slug_url_kwarg = "id"

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        return {**super(PostUpdateView, self).get_context_data(**kwargs), "id": self.kwargs[self.slug_url_kwarg]}

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.none()
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse("post_edit_detail", args=(self.object.slug, self.object.id))


class PostDeleteView(DeleteView):
    template_name = "web/post_delete.html"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.none()
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse("profile_user_posts")


class ProfileView(ListView):
    template_name = "web/profile_post_stats.html"
    model = Post


class ProfileUserEditView(UpdateView):
    model = User
    form_class = ProfileUserChangeForm
    template_name = "web/profile_edit.html"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_success_url(self):  # message данные успешно сохранены
        return reverse("user_profile_edit", args=(self.kwargs["id"],))


class ProfileSettings(UpdateView):
    model = User
    form_class = ProfileSettingsForm
    template_name = "web/profile_settings.html"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_success_url(self):
        return reverse("user_profile_settings", args=(self.kwargs["id"],))


class ProfileUserPostsView(ListView):
    template_name = "web/user_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.none()
        queryset = Post.objects.filter(author=self.request.user).order_by("publish")
        return self.filter_queryset(queryset)

    def filter_queryset(self, posts):

        self.published_posts = "published_posts" in self.request.GET
        self.draft_posts = "draft_posts" in self.request.GET

        if self.published_posts:
            posts = posts.filter(status=Status.published)

        if self.draft_posts:
            posts = posts.filter(status=Status.draft)

        return posts

    def get_context_data(self, *, object_list=None, **kwargs):

        if not self.request.user.is_authenticated:
            return {}
        return {
            **super(ProfileUserPostsView, self).get_context_data(),
            "query_params": self.request.GET,
            "published_posts": self.published_posts,
            "draft_posts": self.draft_posts,
        }
