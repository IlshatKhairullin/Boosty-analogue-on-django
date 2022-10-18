from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormMixin
from .forms import UserCreationForm, RegisterUserForm, PostForm, CommentForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import *


class CustomMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': RegisterUserForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class PostListView(ListView):
    queryset = Post.objects.filter(status=Status.published)
    template_name = 'web/main_page.html'
    context_object_name = 'posts'
    paginate_by = 4
    slug_field = 'id'
    slug_url_kwarg = 'id'


class DetailPostView(CustomMessageMixin, DetailView, FormMixin):
    # FormMixin - тк изначально в DetailView нет параметра form_class
    model = Post
    form_class = CommentForm  # сделать редактирование и удаление коммента
    success_msg = 'Комментарий успешно добавлен'
    template_name = 'web/detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):

        form = self.get_form()

        # if login_required():  # выкинуть надпись: для add comm нужно войти на сайт
        #     return redirect('login')

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):  # добавить AJAX чтобы не уезжать наверх после добавления коммента
        return reverse('post_detail', args=(self.kwargs['slug'], self.kwargs[self.slug_url_kwarg]))


class UpdateCommentView(UpdateView, UserPassesTestMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'web/comment_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self, **kwargs):
        return reverse('post_detail', args=(self.kwargs['slug'], self.kwargs['post_id']))

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return redirect('login')


class DeleteCommentView(DeleteView, UserPassesTestMixin):
    model = Comment
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return redirect('login')

    def get_success_url(self, **kwargs):
        return reverse('post_detail', args=(self.kwargs['slug'], self.kwargs['post_id']))


class DetailPostEditView(DetailView):
    model = Post
    template_name = 'web/post_edit_detail.html'
    context_object_name = 'post'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        return {
            **super(DetailPostEditView, self).get_context_data(**kwargs),
            'id': self.kwargs[self.slug_url_kwarg]
        }


class PostCreateFormView(CreateView):
    template_name = 'web/post_add_edit_form.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile')


class PostUpdateView(UpdateView):
    template_name = 'web/post_add_edit_form.html'
    form_class = PostForm
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        return {
            **super(PostUpdateView, self).get_context_data(**kwargs),
            'id': self.kwargs[self.slug_url_kwarg]
        }

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.none()
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('post_edit_detail', args=(self.object.slug, self.object.id))


class PostDeleteView(DeleteView):
    template_name = 'web/post_delete.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        return {
            **super(PostDeleteView, self).get_context_data(**kwargs),
            'id': self.kwargs[self.slug_url_kwarg]
        }

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.none()
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('profile')


class ProfileView(ListView):
    template_name = 'web/profile.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.none()
        queryset = Post.objects.filter(author=self.request.user).order_by('publish')
        return self.filter_queryset(queryset)

    def filter_queryset(self, posts):

        self.published_posts = 'published_posts' in self.request.GET
        self.draft_posts = 'draft_posts' in self.request.GET

        if self.published_posts:
            posts = posts.filter(status=Status.published)

        if self.draft_posts:
            posts = posts.filter(status=Status.draft)

        return posts

    def get_context_data(self, *, object_list=None, **kwargs):

        if not self.request.user.is_authenticated:
            return {}
        return {
            **super(ProfileView, self).get_context_data(),
            'query_params': self.request.GET,
            'published_posts': self.published_posts,
            'draft_posts': self.draft_posts
        }
