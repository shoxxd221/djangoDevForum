from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *


urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('categories/', AllCategories.as_view(), name='categories'),
    path('category/<slug:category_slug>/', PostsByCategory.as_view(), name='category'),
    path('category/<slug:category_slug>/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('user/<slug:user_slug>', ShowUser.as_view(), name='user'),
    path('posts/', AllPosts.as_view(), name='posts'),
    path('my_posts/', MyPosts.as_view(), name='my_posts'),
    path('all_users/', AllUsers.as_view(), name='all_users'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('about/', About.as_view(), name='about'),
    path('registration/', Register.as_view(), name='registration'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('add_category/', AddCategory.as_view(), name='add_category'),
    path('my_profile/', MyProfile.as_view(), name='profile'),
    path('edit_profile/', EditMyProfile.as_view(), name='edit_profile')
]
