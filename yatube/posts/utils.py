from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render
from posts.models import Follow


def paginator_render_page(list_for_render, request):
    """Функция принимает нужные посты и request,
    выдает на выходе экземпляр объекта Paginator,
    для запрошенного номера страницы.
    """
    return Paginator(
        list_for_render, settings.COUNT_OBJECTS_IN_PAGE
    ).get_page(request.GET.get('page'))


def render_profile(request, profile_user):
    render_button_following = (
        False
        if not request.user.is_authenticated or request.user == profile_user
        else True
    )
    following = (
        True
        if request.user.is_authenticated
        and len(Follow.objects.filter(
            user=request.user
        ).filter(author=profile_user.id)) != 0
        else False
    )
    return render(request, 'posts/profile.html', {
        'author': profile_user,
        'page_obj': paginator_render_page(
            profile_user.posts.select_related('group').all(), request
        ),
        'following': following,
        'render_button_following': render_button_following
    })
