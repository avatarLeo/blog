from django.shortcuts import render
from blog.models import Post, Page
from django.core.paginator import Paginator
from django.db.models import Q


PER_PAGE = 9

def index(request):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
       request, 'blog/pages/index.html',
       {
           'page_obj': page_obj,
       }
    )


def created_by(request, author_pk):
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
       request, 'blog/pages/index.html',
       {
           'page_obj': page_obj,
       }
    )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
       request, 'blog/pages/index.html',
       {
           'page_obj': page_obj,
       }
    )


def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
       request, 'blog/pages/index.html',
       {
           'page_obj': page_obj,
       }
    )

def page(request, slug):
    page = Page.objects.filter(is_published=True).filter(slug=slug).first()
    print(page.title)
    return render(
       request, 'blog/pages/pages.html',
       {
           'page':page
       }
    )

def search(request):

    term = request.GET.get('search', '').strip()
    posts = Post.objects.get_published().filter(
        Q(title__icontains=term) |
        Q(excerpt__icontains=term) |
        Q(content__icontains=term) 
        )[:PER_PAGE]

    return render(
       request, 'blog/pages/index.html',
       {
           'page_obj': posts, 'term': term
       }
    )



def post(request, slug):
    post = Post.objects.get(slug=slug)
    return render(
       request, 'blog/pages/post.html',
       {
           'post': post
       }
    )