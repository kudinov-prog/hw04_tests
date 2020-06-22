from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import PostForm
from .models import Post, Group, User

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
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html',
                  {'page': page, 'paginator': paginator, 'profile': user})


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id)
    count = Post.objects.filter(author=user).count()
    return render(request, 'post.html',
                  {'profile': user, 'post': post, 'count': count})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, username=username)
    post_url = reverse('post', args=(post.author, post_id))
    if user != request.user:
        return redirect(post_url)
    form = PostForm(request.POST or None, instance=post)
    if  form.is_valid():
        post.save()
        return redirect(post_url)
    return render(request, 'new.html', {'form': form, 'post': post})
