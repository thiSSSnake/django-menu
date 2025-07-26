from django.urls import resolve, Resolver404


def get_current_path(context):
    """
    Вспомогательная функция
    Для получения текущего пути из request.path
    """
    request = context["request"]
    current_path = request.path
    return current_path

def get_current_url(context):
    """
    Вспомогательная функция для разрешения
    текущего URL, возвращает текущее имя URL-паттерна
    """
    current_path = get_current_path(context)

    try:
        resolved_url = resolve(current_path)
        current_url_name = resolved_url.url_name
    except Resolver404:
        current_url_name = None
    return current_url_name


