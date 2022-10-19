from django.conf import settings
from django.core.paginator import Paginator


def paginator_render_page(list_for_render, request):
    """Функция принимает нужные посты и request,
    выдает на выходе экземпляр объекта Paginator,
    для запрошенного номера страницы.
    """
    return Paginator(
        list_for_render, settings.COUNT_OBJECTS_IN_PAGE
    ).get_page(request.GET.get('page'))
