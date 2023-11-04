import datetime

from django.shortcuts import render, get_object_or_404

from .models import Post, Category

POST_LIMIT = 5


def get_published_posts():
    return Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(pub_date__lte=datetime.datetime.now(), is_published=True)


def index(request):
    posts = get_published_posts().filter(category__is_published=True
                                         ).order_by('-pub_date')[:POST_LIMIT]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, id):
    post = get_object_or_404(
        get_published_posts().filter(
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
    posts = get_published_posts().filter(
        category=category
    )
    return render(request, 'blog/category.html',
                  {'category': category, 'post_list': posts})
