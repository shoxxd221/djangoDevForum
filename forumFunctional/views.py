from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


from .forms import *
from .utils import *


def is_staff(user):
    return user.is_authenticated and user.is_staff


class Index(DataMixin, TemplateView):
    template_name = 'forumFunctional/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='developmentForum')
        return dict(list(context.items()) + list(c_def.items()))


class AllCategories(DataMixin, TemplateView):
    template_name = 'forumFunctional/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        c_def = self.get_user_context(title='Categories')
        return dict(list(context.items()) + list(c_def.items()))


class AllPosts(DataMixin, ListView):
    template_name = 'forumFunctional/posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Posts')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.select_related('user', 'category').all()


class PostsByCategory(DataMixin, TemplateView):
    template_name = 'forumFunctional/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs.get("category_slug"))
        context['posts'] = Post.objects.select_related('category').filter(category=category)
        c_def = self.get_user_context(title=f'Posts of {category.title} category')
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DataMixin, CreateView):
    form_class = AddCommentForm
    template_name = 'forumFunctional/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.select_related('user').get(slug=self.kwargs.get("post_slug"))
        context['post'] = post
        context['comments'] = Comment.objects.select_related('user').filter(post_id=post.pk)
        c_def = self.get_user_context(title=post.title)
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'category_slug': self.object.post.category.slug, 'post_slug': self.object.post.slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.post = Post.objects.get(slug=self.kwargs['post_slug'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())



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
        user = self.request.user
        context['posts'] = Post.objects.select_related('category').filter(user=user)
        comments = Comment.objects.select_related('post__category').filter(user=user)
        context['commented_posts'] = [comment.post for comment in comments]
        c_def = self.get_user_context(title='My profile')
        return dict(list(context.items()) + list(c_def.items()))


class EditMyProfile(LoginRequiredMixin, DataMixin, UpdateView):
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


class MyPosts(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'forumFunctional/my_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.select_related('category').filter(user=self.request.user)
        c_def = self.get_user_context(title='My posts')
        return dict(list(context.items()) + list(c_def.items()))


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'forumFunctional/add_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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


class AllUsers(DataMixin, ListView):
    template_name = 'forumFunctional/all_users.html'
    context_object_name = 'all_users'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='All users')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return User.objects.all()


class ShowUser(DataMixin, TemplateView):
    template_name = 'forumFunctional/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs.get('user_slug'))
        context['posts'] = Post.objects.select_related('category').filter(user=user)
        comments = Comment.objects.select_related('post__category').filter(user=user)
        context['commented_posts'] = [comment.post for comment in comments]
        c_def = self.get_user_context(title=user.username)
        return dict(list(context.items()) + list(c_def.items()))


class About(DataMixin, TemplateView):
    template_name = 'forumFunctional/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='About')
        return dict(list(context.items()) + list(c_def.items()))


def logout_user(request):
    logout(request)
    return redirect('login')
