from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *


urlpatterns = [
    path('', ForumView.as_view(), name='home'),
    path('categories/', Categories.as_view(), name='categories'),
    path('category/<slug:category_slug>/', ShowCategory, name='category'),
    path('category/<slug:category_slug>/<slug:post_slug>/', ShowPost, name='post'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('about/', About.as_view(), name='about'),
    path('registration/', Register.as_view(), name='registration'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('add_category/', AddCategory.as_view(), name='add_category'),
    path('my_profile/', MyProfile.as_view(), name='profile'),
    path('edit_profile/', EditProfile.as_view(), name='edit_profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)