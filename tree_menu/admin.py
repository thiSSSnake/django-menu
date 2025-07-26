from django.contrib import admin
from .models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели Меню
    """
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели MenuItem
    """
    list_display = (
        'name',
        'menu',
        'parent',
        'url',
        'named_url',
        'order',
    )
    list_filter = ('menu', 'parent',)
    search_fields = ('name', 'url', 'named_url',)
    raw_id_fields = ('parent',)
    fieldsets = (
        (None, {
            'fields': ('menu', 'name', 'parent', 'order')
        }),
        ('URL Information', {
            'fields': ('url', 'named_url'),
            'description': "Укажите либо явный URL, либо именованный URL. Не оба."
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('menu', 'parent')
