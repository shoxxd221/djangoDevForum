from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


from .forms import *
from .utils import *


def is_staff(user):
    return user.is_authenticated and user.is_staff


class ForumView(DataMixin, TemplateView):
    template_name = 'forumFunctional/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='developmentForum')
        return dict(list(context.items()) + list(c_def.items()))


class Categories(DataMixin, TemplateView):
    template_name = 'forumFunctional/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        c_def = self.get_user_context(title='Categories')
        return dict(list(context.items()) + list(c_def.items()))


def ShowCategory(request, category_slug):
    return HttpResponse(f'This is a {category_slug}')


def ShowPost(request, category_slug, post_slug):
    return HttpResponse(f'url = {category_slug}/{post_slug}')


class Register(UserPassesTestMixin, DataMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'forumFunctional/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registration')
        return dict(list(context.items()) + list(c_def.items()))

    def test_func(self):
        return not self.request.user.is_authenticated


class About(DataMixin, TemplateView):
    template_name = 'forumFunctional/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='About')
        return dict(list(context.items()) + list(c_def.items()))


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'forumFunctional/add_post.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add post')
        return dict(list(context.items()) + list(c_def.items()))


class AddCategory(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddCategoryForm
    template_name = 'forumFunctional/add_category.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add category')
        return dict(list(context.items()) + list(c_def.items()))

    @method_decorator(user_passes_test(is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class Login(UserPassesTestMixin, DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'forumFunctional/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

    def test_func(self):
        return not self.request.user.is_authenticated


class MyProfile(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'forumFunctional/my_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        comments = Comment.objects.filter(user_id=self.request.user.pk)
        # Get list of commented posts
        commented_posts = []
        for i in comments:
            if i.user_id == self.request.user.pk:
                commented_posts.append(Post.objects.get(user_id=i.user_id))
        context['commented_posts'] = list(set(commented_posts))
        c_def = self.get_user_context(title='My profile')
        return dict(list(context.items()) + list(c_def.items()))


class EditProfile(LoginRequiredMixin, DataMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'forumFunctional/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Edit profile')
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        form.save()
        return redirect('profile')


def logout_user(request):
    logout(request)
    return redirect('login')
