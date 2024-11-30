
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import now
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


def index(request):
    post_list = Post.objects.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog/index.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = category.post_set.filter(
        pub_date__lte=now(),
        is_published=True
    ).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, 'blog/category.html', context)


def post_detail(request, pk):
    post = get_object_or_404(
        Post,
        pk=pk,
    )
    if request.user == post.author:
        form = CommentForm()
        comments = post.comment.all()
        context = {
            'post': post,
            'comments': comments,
            'form': form if request.user.is_authenticated else None
        }
        return render(request, 'blog/detail.html', context)
    
    if not post.is_published:
        raise Http404
    if post.pub_date > now():
        raise Http404
    if not post.category or not post.category.is_published:
        raise Http404
    
    form = CommentForm()
    comments = post.comment.all()
    context = {
        'post': post,
        'comments': comments,
        'form': form if request.user.is_authenticated else None
    }
    return render(request, 'blog/detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


@login_required(login_url='login')
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user: 
        return redirect('blog:post_detail', pk=post.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form, 'is_edit': True})


@login_required
def post_delete(request, post_id):
    template_name = 'blog/create.html'
    delete_post = get_object_or_404(
        Post, pk=post_id, author__username=request.user
    )
    if request.method != 'POST':
        context = {
            'post': delete_post,
            'is_delete': True,
        }
        return render(request, template_name, context)
    if delete_post.author == request.user:
        delete_post.delete()
    return redirect('blog:profile', request.user)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=post_id)
    else:
        form = CommentForm()
    context = {
        'form': form,
        'post': post,
        'comments': post.comment.all()
    }
    return render(request, 'blog/detail.html', context)


@login_required
def comment_edit(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    if comment.author != request.user:
        raise Http404("Вы не можете редактировать этот комментарий.")

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", pk=post.id)
    else:
        form = CommentForm(instance=comment)

    context = {
        "form": form,
        "is_edit": True,
        "post": post
    }
    return render(request, "blog/create.html", context)


@login_required
def comment_delete(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if comment.author != request.user:
        raise Http404("Вы не можете удалить этот комментарий.")
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", pk=post.id)
    context = {
        "object": comment,
        "type": "comment"
    }
    return render(request, "blog/comment.html", context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {'form': form})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(
        author=profile
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'blog/user.html', {'form': form})
