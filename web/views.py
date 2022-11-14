from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormMixin
from .forms import UserCreationForm, RegisterUserForm, PostForm, CommentForm, ProfileUserChangeForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

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
    template_name = 'web/main_page.html'
    context_object_name = 'posts'
    paginate_by = 20
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_queryset(self):
        queryset = Post.objects.filter(status=Status.published)

        if 'popularity_post' in self.request.GET:
            queryset = queryset.annotate(
                total_views=Count('views', distinct=True)
            ).order_by('-total_views')
        elif 'rating_post' in self.request.GET:
            queryset = queryset.annotate(
                total_likes=Count('likes', distinct=True)
            ).order_by('-total_likes')

        return self.filter_queryset(queryset)

    def filter_queryset(self, posts):
        self.search = self.request.GET.get("search", None)

        if self.search:
            # Q - спец объект, у которого определены логические операции (и, или...)
            posts = posts.filter(
                Q(title__icontains=self.search) |
                Q(body__icontains=self.search)
            )
        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            **super(PostListView, self).get_context_data(**kwargs),
            'most_popular_tags': Post.tags.most_common()[:4],
            'search': self.request.GET.get('search')
        }


def LikePostView(request, post_slug, post_id):
    if 'post_like_post_detail' in request.POST:
        if request.user.is_authenticated:
            post = get_object_or_404(Post, id=request.POST.get('post_like_post_detail'))
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            return HttpResponseRedirect(reverse('post_detail', args=(post_slug, post_id)))
        else:
            return HttpResponseRedirect(reverse('register'))  # message to do

    if 'post_like_main_page':
        if request.user.is_authenticated:
            post = get_object_or_404(Post, id=request.POST.get('post_like_main_page'))
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            return HttpResponseRedirect(reverse('post_list'))
        else:
            return HttpResponseRedirect(reverse('register'))  # message to do

    if 'comment_like' in request.POST:
        if request.user.is_authenticated:
            comment = get_object_or_404(Comment, id=request.POST.get('comment_like'))
            if comment.likes.filter(id=request.user.id).exists():
                comment.likes.remove(request.user)
            else:
                comment.likes.add(request.user)
            return HttpResponseRedirect(
                reverse('post_detail', args=(post_slug, post_id)))
        else:
            return HttpResponseRedirect(reverse('register'))  # message to do


class TagIndexView(ListView):
    model = Post
    template_name = 'web/main_page.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug'))

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            **super(TagIndexView, self).get_context_data(**kwargs),
            'most_popular_tags': Post.tags.most_common()[:4],
        }


class DetailPostView(CustomMessageMixin, FormMixin, DetailView, UserPassesTestMixin):
    # FormMixin - тк изначально в DetailView нет параметра form_class
    model = Post
    form_class = CommentForm
    success_msg = 'Комментарий успешно добавлен'
    template_name = 'web/detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def test_func(self):  # выкинуть надпись: для add comm нужно войти на сайт
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return redirect('login')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.parent_obj = None

        try:  # проверка на тот случай, если к нам прилетел не тот parent_id откуда то еще
            parent_id = int(request.POST.get('parent_id'))
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
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.author = self.request.user
        self.object.parent = self.parent_obj
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['id'])
        total_post_likes = post.number_of_likes()
        total_views = post.number_of_views()

        if self.request.user.is_authenticated:
            post.views.add(self.request.user)

        post_liked = False
        if post.likes.filter(id=self.request.user.id):
            post_liked = True

        return {
            **super(DetailPostView, self).get_context_data(**kwargs),
            'total_post_likes': total_post_likes,
            'post_liked': post_liked,
            'post_views': total_views,
        }

    def get_success_url(self, **kwargs):
        return reverse('post_detail', args=(self.kwargs['slug'], self.kwargs[self.slug_url_kwarg]))


class UpdateCommentView(UpdateView, UserPassesTestMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'web/comment_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        return {
            **super(UpdateCommentView, self).get_context_data(**kwargs),
            'slug': self.kwargs['slug'],
            'post_id': self.kwargs['post_id']
        }

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
        return reverse('profile_user_posts')


class PostUpdateView(UpdateView):
    template_name = 'web/post_add_edit_form.html'
    form_class = PostForm
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def form_valid(self, form):
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

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.none()
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('profile_user_posts')


class ProfileView(ListView):
    template_name = 'web/profile_post_stats.html'
    model = Post


class ProfileUserEditView(UpdateView):
    model = AuthorInfo
    form_class = ProfileUserChangeForm
    template_name = 'web/profile_edit.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):  # message данные успешно сохранены
        return reverse('user_profile_edit', args=(self.kwargs['id'],))


class ProfileUserPostsView(ListView):
    template_name = 'web/user_posts.html'
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
            **super(ProfileUserPostsView, self).get_context_data(),
            'query_params': self.request.GET,
            'published_posts': self.published_posts,
            'draft_posts': self.draft_posts
        }
