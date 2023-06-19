from .models import *


menu = [{'title': "Home", 'url_name': 'home'},
        {'title': "About", 'url_name': 'about'},
        {'title': "Categories", 'url_name': 'categories'},
        {'title': 'Add post', 'url_name': 'add_post'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['users'] = User.objects.all()
        return context
