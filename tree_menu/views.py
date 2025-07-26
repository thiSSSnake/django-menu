from django.shortcuts import render

def home_view(request):
    """
    Простое представление для главной страницы.
    """
    return render(request, 'tree_menu/home.html', {'page_title': 'Главная страница'})

def page_view(request, page_name):
    """
    Простое представление для демонстрации различных страниц.
    Используется для явных URL-ов типа /page/about/, /page/services/, etc.
    """
    return render(request, 'tree_menu/page.html', {'page_title': f'Страница: {page_name}'})

def named_page_view(request):
    """
    Представление для демонстрации именованного URL 'tree_menu:named_page'.
    """
    return render(request, 'tree_menu/named_page.html', {'page_title': 'Именованная страница (Контакты)'})

def services_view(request):
    """
    Представление для страницы 'Услуги', если она будет использоваться как именованный URL.
    """
    return render(request, 'tree_menu/page.html', {'page_title': 'Страница Услуг (Именованная)'})

def consulting_view(request):
    """
    Представление для страницы 'Консалтинг', если она будет использоваться как именованный URL.
    """
    return render(request, 'tree_menu/page.html', {'page_title': 'Страница Консалтинга (Именованная)'})

def development_view(request):
    """
    Представление для страницы 'Разработка', если она будет использоваться как именованный URL.
    """
    return render(request, 'tree_menu/page.html', {'page_title': 'Страница Разработки (Именованная)'})