from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'email', 'is_staff')
    search_fields = ('id', 'username', 'email')
    list_editable = ('password', 'is_staff')
    list_filter = ('username', )


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'category_id', 'user_id', 'time_update')
    search_fields = ('id', 'title', 'time_create', 'category_id', 'user_id', 'time_update')
    list_filter = ('title', )


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
