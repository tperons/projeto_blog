from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('page/<slug:slug>/', Page.as_view(), name='page'),
    path('post/<slug:slug>/', Posts.as_view(), name='post'),
    path('author/<int:author_pk>/', Author.as_view(), name='author'),
    path('category/<slug:slug>/', Category.as_view(), name='category'),
    path('tag/<slug:slug>/', Tag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
]
