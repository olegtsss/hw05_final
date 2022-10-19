from core.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import CommentForm, PostForm
from posts.models import Comment, Follow, Group, Post
from posts.utils import paginator_render_page


def render_profile(request, profile_user):
    following = False
    if (request.user.is_authenticated
        and request.user != profile_user
        and Follow.objects.filter(user=request.user).
            filter(author=profile_user.id).
            exists()):
        following = True
    return render(request, 'posts/profile.html', {
        'author': profile_user,
        'page_obj': paginator_render_page(
            profile_user.
            posts_post_related.select_related('group').all(), request
        ),
        'following': following,
        'all_following': len(Follow.objects.filter(user=profile_user)),
        'all_follower': len(Follow.objects.filter(author=profile_user)),
        'all_comments': len(Comment.objects.filter(author=profile_user))
    })


def index(request):
    return render(request, 'posts/index.html', {
        'page_obj': paginator_render_page(
            Post.objects.select_related('author', 'group').all(), request
        ),
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
            'form': CommentForm(),
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
    if form.is_valid() and Post.objects.filter(id=post_id).exists():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = Post.objects.get(id=post_id)
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.select_related(
        'author', 'group'
    ).filter(author__following__user=request.user)
    return render(request, 'posts/follow.html', {
        'page_obj': paginator_render_page(posts, request)
    })


@login_required
def profile_follow(request, username):
    profile_user = get_object_or_404(User, username=username)
    if (request.user != profile_user
        and not Follow.objects.filter(
            user=request.user).filter(author=profile_user).exists()):
        Follow.objects.create(user=request.user, author=profile_user)
    return render_profile(request, profile_user)


@login_required
def profile_unfollow(request, username):
    profile_user = get_object_or_404(User, username=username)
    link = get_object_or_404(Follow, user=request.user, author=profile_user)
    link.delete()
    return(render_profile(request, profile_user))
