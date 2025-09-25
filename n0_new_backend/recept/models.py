from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from foodgram.constants import (
    AMOUNT_INGREDIENTS_MIN,
    COOKING_TIME_MIN,
    TEXT_LENGTH_MAX,
    TEXT_LENGTH_MEDIUM,
    TEXT_LENGTH_MIN,
)

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингридентов."""
    name = models.CharField('Название', max_length=TEXT_LENGTH_MEDIUM)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=TEXT_LENGTH_MIN)

    class Meta:
        default_related_name = 'ingredients'
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=TEXT_LENGTH_MAX, unique=True, verbose_name='Название тега')
    slug = models.SlugField(unique=True, verbose_name='SLUG')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор')
    name = models.CharField(
        max_length=TEXT_LENGTH_MAX, verbose_name='Название')
    image = models.ImageField(
        upload_to='recipes', verbose_name='Изображение')
    text = models.TextField(
        verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги')
    short_link = models.CharField(
        'Короткая ссылка',
        max_length=TEXT_LENGTH_MIN,
        blank=True,
        unique=True,
        null=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=[
            MinValueValidator(COOKING_TIME_MIN)
        ],
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель связи рецепта и ингридиента"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_links'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_links'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(
                AMOUNT_INGREDIENTS_MIN,
                f'Минимальное количство {AMOUNT_INGREDIENTS_MIN}'
            ),
        )
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('recipe',)
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='unique_recipe_ingredient',
            ),
        )


class Favorite(models.Model):
    """Модель избранных рецептов"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites', verbose_name='<UNK>')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites')

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user.username} добавил в избранное {self.recipe.name}'


class ShoppingCart(models.Model):
    """Модель избранного и покупок"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
