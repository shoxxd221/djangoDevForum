from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    photo = models.ImageField(
        upload_to='photos/users/',
        blank=True,
        null=True,
        verbose_name='Photo of user'
    )

    class Meta:
        ordering = ['username']

    def get_absolute_url(self):
        return reverse('user', kwargs={'user_slug': self.username})


class Category(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='Category name'
    )
    slug = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='URL'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class Post(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='Post name'
    )
    slug = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='URL'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Name of category'
    )
    content = models.TextField(
        verbose_name='Content of post'
    )
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Photo in post'
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date of creation'
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Update date'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Username'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'category_slug': self.category.slug ,'post_slug': self.slug})


class Comment(models.Model):
    content = models.TextField(
        unique=True,
        verbose_name='Content of comment'
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date of creation'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='Post title'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Username'
    )

    class Meta:
        ordering = ['post']

    def __str__(self):
        return f"{self.user.username} commented {self.post.title}"
