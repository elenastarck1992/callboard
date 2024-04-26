from django.contrib import admin

from ads.models import Ad, Comment


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Отображение списка объявлений"""
    list_display = ('id', 'title', 'price', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Отображение списка отзывов"""
    list_display = ('id', 'text', 'author', 'ad')
