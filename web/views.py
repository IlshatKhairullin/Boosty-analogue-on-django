from django.views import View
from django.views.generic import ListView, DetailView
from .forms import UserCreationForm, RegisterUserForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import *


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
    queryset = Post.objects.all()
    template_name = 'web/main_page.html'
    context_object_name = 'posts'
    paginate_by = 4


class DetailPostView(DetailView):
    model = Post
    template_name = 'web/detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post'

