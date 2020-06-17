from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html",
                  {"group": group, "page": page, "paginator": paginator})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'new.html', {'form': form})
    form = PostForm()
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user)
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page': page, 'paginator': paginator, 'post_list': post_list})


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post_single = Post.objects.filter(id=post_id)
    post_list = Post.objects.filter(author=user)
    return render(request, 'post.html', {'post_single': post_single, 'post_list': post_list})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, username=username)
    if user == request.user:
        form = PostForm(request.POST, instance=post)
        if request.method == 'POST' and form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post', username=post.author.username, post_id=post_id)
        form = PostForm(instance=post)
        return render(request, 'new.html', {'form': form, 'post': post})
    return redirect('post', username=post.author.username, post_id=post_id)
