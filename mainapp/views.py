from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag, get_slug
from django.views.generic import View
from .utils import ObjectDetailMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q


def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    posts = Post.objects.all()
    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())

    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }
    return render(request, 'blog/index.html', context=context)


class PostDetail(ObjectDetailMixin, View):

    model = Post
    template = 'blog/post_detail.html'


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):

    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):

    form_model = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):

    form_model = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


class TagUpdate(ObjectUpdateMixin, View):

    model = Tag
    form_model = TagForm
    template = 'blog/tag_update_form.html'


class PostUpdate(ObjectUpdateMixin, View):
    model = Post
    form_model = PostForm
    template = 'blog/post_update_form.html'


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):

    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):

    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True






