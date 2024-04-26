from rest_framework import serializers
from ads.models import Ad, Comment


class AdSerializer(serializers.ModelSerializer):
    """Класс сериализатора для предпросмотра объявлений"""

    class Meta:
        model = Ad
        fields = ('title', 'price', 'description', 'image')


class CommentSerializer(serializers.ModelSerializer):
    """Класс сериализатора для отзыва"""

    class Meta:
        model = Comment
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    """Класс сериализатора для просмотра одного объявления"""

    comment = CommentSerializer(source='comment_ad', read_only=True, many=True)

    class Meta:
        model = Ad
        fields = '__all__'
