from django.views.generic.base import View
from .utils import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

# list
def posts_list(request):
    search_query = request.GET.get('q', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()
    if page.has_previous():
        previous_url = f'{page.previous_page_number()}'
    else:
        previous_url = ''

    if page.has_next():
        next_url = f'{page.next_page_number()}'
    else:
        next_url = ''
    return render(request, 'blog/post/posts_list.html', context={'posts': page,
                                                                 'is_paginated': is_paginated,
                                                                 'next_url': next_url,
                                                                 'previous_url': previous_url})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag/tags_list.html', locals())


# detail
class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post/post_detail.html'

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag/tag_detail.html'


# create
class TagCreate(LoginRequiredMixin,ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag/tag_create.html'
    raise_exception = True

class PostCreate(LoginRequiredMixin,ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post/post_create.html'
    raise_exception = True


# update
class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag/tag_update.html'
    raise_exception = True

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post/post_update.html'
    raise_exception = True


# delete
class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag/tag_delete.html'
    redirect_url = 'tags_list'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post/post_delete.html'
    redirect_url = 'blog'
    raise_exception = True
