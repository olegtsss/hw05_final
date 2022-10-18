from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import CommentForm, PostForm
from posts.models import Comment, Follow, Group, Post, User
from posts.utils import paginator_render_page, render_profile


def index(request):
    return render(request, 'posts/index.html', {
        'page_obj': paginator_render_page(
            Post.objects.select_related('author', 'group').all(), request
        ),
        'index': True
    })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    return render(request, 'posts/group_list.html', {
        'group': group,
        'page_obj': paginator_render_page(
            group.posts.select_related('author').all(), request
        ),
    })


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    return(render_profile(request, profile_user))


def post_detail(request, post_id):
    return render(
        request, 'posts/post_detail.html',
        {
            'post': get_object_or_404(Post, id=post_id),
            'new_comment_form': CommentForm(),
            'page_obj': paginator_render_page(
                Comment.objects.select_related(
                    'author', 'post'
                ).filter(post=post_id), request
            )
        }
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {"form": form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {"form": form})
    form.save()
    return redirect('posts:post_detail', post_id)


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = Post.objects.get(id=post_id)
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    follows = Follow.objects.filter(user=request.user)
    posts = []
    for follow in follows:
        for post in Post.objects.select_related(
            'author', 'group'
        ).filter(author=follow.author):
            posts.append(post)
    context = {
        'page_obj': paginator_render_page(posts, request),
        'follow': True
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    profile_user = get_object_or_404(User, username=username)
    if (
        request.user != profile_user
        and len(Follow.objects.filter(
            user=request.user).filter(author=profile_user)) == 0
    ):
        Follow.objects.create(user=request.user, author=profile_user)
    return(render_profile(request, profile_user))


@login_required
def profile_unfollow(request, username):
    profile_user = get_object_or_404(User, username=username)
    Follow.objects.get(user=request.user, author=profile_user).delete()
    return(render_profile(request, profile_user))
