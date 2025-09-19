from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    '''Модель пользователя.'''
    email = models.EmailField(
        unique=True,
        max_length=256,
        validators=[MaxLengthValidator(256)],
        verbose_name='Электронная почта пользователя',
        help_text='Введите свой электронный адрес'
    )

    username = models.CharField(
        max_length=256,
        unique=True,
        help_text=(
            'Обязательное поле. 150 символов или меньше. '
            'Только буквы, цифры и @/./+/-/_ символы.'
        ),
        validators=[
            validate_username,
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=(
                    'Username пользователя может содержать только '
                    'буквы, цифры и @/./+/-/_ символы.'
                ),
            ),
        ],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
        verbose_name='Имя пользователя',
    )

    first_name = models.CharField(
        max_length=256,
        validators=[MaxLengthValidator(256)],
        verbose_name='Имя'
    )

    last_name = models.CharField(
        max_length=256,
        validators=[MaxLengthValidator(256)],
        verbose_name='Фамилия'
    )

    password = models.CharField(max_length=256, verbose_name='Пароль')
    avatar = models.ImageField(blank=True, null=True,
                               verbose_name='Изображение пользователя')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Подписка на автора."""

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscribers',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='authors',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('subscriber',)
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='unique_subscriber_author'
            ),
            models.CheckConstraint(
                name='check_subscriber_author',
                check=~models.Q(subscriber=models.F('author')),
            )
        ]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'
