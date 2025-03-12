from django.shortcuts import render
from django.core.paginator import Paginator




posts = list(range(1000))




def index(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/index.html',
        {'page_obj': page_obj,}
    )




def page(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'pages/page.html',
        {'page_obj': page_obj,}
    )




def post(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'pages/post.html',
        {'page_obj': page_obj,}
    )
