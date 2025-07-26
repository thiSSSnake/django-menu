from django.db import models
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ValidationError

class Menu(models.Model):
    """
    Модель меню - для определения по названию.
    Каждое название - уникально.
    """
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Название меню"
    )

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    """
    Модель отдельного пункта меню.
    Может иметь явный/именованый url
    """
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Меню'
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название пункта"
    )
    url = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Явный URL"
    )
    named_url = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Именованный URL"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительский пункт"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Порядок сортировки"
    )

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

        constraints = [
            models.UniqueConstraint(
                fields=['menu', 'parent', 'name'],
                name="unique_menu_parent_name"
            )
        ]
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.menu.name})"
    
    def clean(self):
        """
        Валидация.
        Указан либо явный url, либо именнованый.
        """
        if self.url and self.named_url:
            raise ValidationError(
                "Должен быть указан один из вариантов: либо 'Явный URL' либо 'Именнованый URL'."
            )
        if not self.url and not self.named_url:
            raise ValidationError(
                "Необходимо указать либо 'Явный URL' либо 'Именнованый URL'."
            )
    
    def get_absolute_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return "#invalid-named-url"
        return self.url
