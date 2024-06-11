from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from blog.models import Post, Page, Tag
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
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

class CategoryListView(PostListView):

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(category__slug=self.kwargs.get('slug'))
       
        if not queryset:
            raise Http404
        
        self._context_temp = queryset[0].category.name
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Categoria - ' + self._context_temp
        return context


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(tags__slug=self.kwargs.get('slug'))
    
    
    def get_context_data(self, **kwargs):
        tag = Tag.objects.filter(slug=self.kwargs.get('slug')).first()
        context = super().get_context_data(**kwargs)
        page_title = 'Tag - ' + tag.name
        print(page_title)
        context['page_title'] = page_title
        return context
    

class SearchListView(PostListView):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get('search').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        term = self._search_value
        return super().get_queryset().filter(
        Q(title__icontains=term) |
        Q(excerpt__icontains=term) |
        Q(content__icontains=term) 
        )[:PER_PAGE]
    
    def get_context_data(self, **kwargs):
        page_title = f'{self._search_value} search - '
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': page_title[:30],
            'term': self._search_value
        })
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)
    

def page(request, slug):
    page = Page.objects.filter(is_published=True).filter(slug=slug).first()


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