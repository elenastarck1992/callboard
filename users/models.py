from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Класс для создания модели пользователя"""
    username = None
    first_name = models.CharField(max_length=150, verbose_name='имя пользователя', blank=True, null=True)
    last_name = models.CharField(max_length=150, verbose_name='фамилия пользователя', blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name='телефон пользователя', blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='почта пользователя')
    image = models.ImageField(upload_to='users/', verbose_name='аватарка пользователя', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
