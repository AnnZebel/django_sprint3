from django.shortcuts import render, get_object_or_404
import datetime

from .models import Post, Category


def index(request):
    posts = Post.objects.select_related(
        'author', 'location'
    ).filter(pub_date__lte=datetime.datetime.now(),
             is_published=True,
             category__is_published=True
             ).order_by('-pub_date')[0:5]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, id):
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            pub_date__lte=datetime.datetime.now(),
            category__is_published=True,
            pk=id
        )
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True)
    posts = category.posts.all().select_related(
        'location',
        'author').filter(
        is_published=True,
        pub_date__lte=datetime.datetime.now()
    )
    return render(request, 'blog/category.html',
                  {'category': category, 'post_list': posts})
