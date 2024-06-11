from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from blog.models import Post, Page
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic.list import ListView


PER_PAGE = 9

class PostListView(ListView):
    model = Post
    paginate_by = PER_PAGE
    context_object_name = 'posts'
    template_name = 'blog/pages/index.html'
    ordering = '-pk',
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home - '
        })
        return context
        

class CreatedByListView(PostListView):

    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(created_by__pk=self.kwargs.get('author_pk'))
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.filter(pk=self.kwargs.get('author_pk')).first()
        
        if user is None:
            raise Http404

        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'

        page_title = user_full_name + ' post - '

        context['page_title'] = page_title

        return context

def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)

    if user is None:
        raise Http404

    user_full_name = user.username

    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'

    page_title = user_full_name + ' post - '

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
       request, 'blog/pages/index.html',
       {
           'page_obj': page_obj,
           'page_title': page_title,
       }
    )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)



    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404
    
    page_title = f'{page_obj[0].category.name} - categorias'
    

    return render(
       request, 'blog/pages/index.html',
       {
           'page_obj': page_obj,
           'page_title': page_title,
       }
    )


def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404
    
    page_title = f'{page_obj[0].tags.first().name} - tag'

    return render(
       request, 'blog/pages/index.html',
       {
           'page_obj': page_obj,
           'page_title': page_title,
       }
    )

def page(request, slug):
    page = Page.objects.filter(is_published=True).filter(slug=slug).first()
    print()

    if page is None:
        raise Http404
    
    page_title = page.title + 'Página'

    return render(
       request, 'blog/pages/pages.html',
       {
           'page':page,
           'page_title': page_title,
       }
    )

def search(request):

    term = request.GET.get('search', '').strip()
    posts = Post.objects.get_published().filter(
        Q(title__icontains=term) |
        Q(excerpt__icontains=term) |
        Q(content__icontains=term) 
        )[:PER_PAGE]
    
    page_title = f'{term[:30]} search - '

    return render(
       request, 'blog/pages/index.html',
       {
           'page_obj': posts, 'term': term,
           'page_title': page_title,
       }
    )



def post(request, slug):
    post = Post.objects.get(slug=slug)
    return render(
       request, 'blog/pages/post.html',
       {
           'post': post,
           'page_title': post.title,
       }
    )