from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from blog.models import Post, Page, Tag
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView


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
    

class PageDetailView(DetailView):
    context_object_name = 'page'
    model = Page
    slug_field = 'slug'
    allow_empty = False
    template_name = 'blog/pages/pages.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title =  'Página - ' + page.title
        context.update({
            'page_title': page_title
        })
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)

    
class PostDetailView(DetailView):
    context_object_name = 'post'
    model = Post
    slug_field = 'slug'
    allow_empty = False
    template_name = 'blog/pages/post.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post_title =  'Post - ' + post.title
        context.update({
            'page_title': post_title
        })
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)





def post(request, slug):
    post = Post.objects.get(slug=slug)
    return render(
       request, 'blog/pages/post.html',
       {
           'post': post,
           'page_title': post.title,
       }
    )