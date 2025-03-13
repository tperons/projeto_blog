from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import *
from django.db.models import Q

POSTS_PER_PAGE = 9


def index(request):
    posts = Post.objects.get_published()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/index.html',
        {'page_obj': page_obj,}
    )




def page(request, slug):
    page = Page.objects.filter(is_published=True).filter(slug=slug).first()

    return render(
        request,
        'pages/page.html',
        {'page': page,}
    )




def post(request, slug):
    post = Post.objects.get_published().filter(slug=slug).first()

    return render(
        request,
        'pages/post.html',
        {'post': post,}
    )









def author(request, author_pk):
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/index.html',
        {'page_obj': page_obj,}
    )




def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/index.html',
        {'page_obj': page_obj,}
    )

def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/index.html',
        {'page_obj': page_obj,}
    )

def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = (
        Post.objects.get_published().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        ))
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/index.html',
        {'page_obj': page_obj, 'search_value': search_value}
    )