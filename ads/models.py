from django.db import models
from django.utils import timezone

from users.models import User


class Ad(models.Model):
    """Класс для создания модели объявления"""
    title = models.CharField(max_length=150, verbose_name='название товара')
    price = models.PositiveIntegerField(verbose_name='цена товара')
    description = models.TextField(verbose_name='описание товара')
    image = models.ImageField(upload_to='ads/', verbose_name='фото товара', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель объявления', null=True,
                               blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='дата и время создания объявления')

    def __str__(self):
        return f'{self.title} {self.price}'

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'
        ordering = ['-created_at']


class Comment(models.Model):
    """Класс для создания модели отзыва"""
    text = models.TextField(verbose_name='текст отзыва')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель отзыва', null=True, blank=True)
    ad = models.ForeignKey(Ad, related_name='comment_ad', on_delete=models.CASCADE,
                           verbose_name='объявление, под которым оставлен отзыв', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='дата и время написания отзыва')

    def __str__(self):
        return f'{self.text} {self.ad}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-created_at']
