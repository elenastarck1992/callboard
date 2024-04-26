from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Класс для пагинации объявлений"""
    page_size = 4  # Количество элементов на странице
