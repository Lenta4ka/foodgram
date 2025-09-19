from django.db import models

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Tags(models.Model):
    """Теги рецептов"""
    name = models.CharField(
        unique=True,
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=256,
        null=True,
        allow_unicode=False,

   )

class Follow(models.Model):
    """Подписка"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower",
        verbose_name="Пользователь"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers",
        verbose_name="Подписчик"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["following", "user"],
                name="unique_follow"
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("following")),
                name="user_cannot_follow_himself"
            ),
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return f"Подписчики: {self.user}"