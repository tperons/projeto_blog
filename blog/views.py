from django.shortcuts import redirect
from blog.models import *
from django.db.models import Q
from django.views.generic import ListView, DetailView
from typing import Any
from django.contrib.auth.models import User
from django.http import Http404




# Class Based View para Index
class Index(ListView):
    model = Post
    template_name = 'pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk'
    paginate_by = 9
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({'page_title': 'Home - '})
        return context
    

# Class Based View para Author (Herda de Index)
class Author(Index):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username
        
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '

        context.update({'page_title': page_title,})
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by__pk=self._temp_context['user'].pk)
        return queryset
    
    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({'author_pk': author_pk, 'user': user,})

        return super().get(request, *args, **kwargs)    
    

# Class Based View para Categoria (Herda de Index)
class Category(Index):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - '
        context.update({'page_title': page_title,})
        return context
    

# Class Based View para Tag (Herda de Index)
class Tag(Index):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(tags__slug=self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].tags.first().name} - '
        context.update({'page_title': page_title,})
        return context
    

# Class Based View para Search (Herda de Index)
class Search(Index):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self):
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self._search_value
        context.update({'page_title': f'{search_value[:30]} - ', 'search_value': search_value})
        return context
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)
    

# Class Based View para Page
class Page(DetailView):
    model = Page
    template_name = 'pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page.title} - '
        context.update({'page_title': page_title})
        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
    

# Class Based View para Page
class Posts(DetailView):
    model = Post
    template_name = 'pages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f'{post.title} - '
        context.update({'page_title': page_title})
        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)