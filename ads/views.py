from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from ads.filters import AdFilter
from ads.models import Ad, Comment
from ads.paginators import CustomPagination
from ads.permissions import IsOwner, IsAdmin
from ads.serializers import AdSerializer, CommentSerializer, AdDetailSerializer


class AdCreateAPIView(generics.CreateAPIView):
    """Класс для создания объявлений"""
    serializer_class = AdDetailSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Метод для автоматической привязки объявления к создателю"""
        serializer.save(author=self.request.user)


class AdListAPIView(generics.ListAPIView):
    """Класс для просмотра списка всех объявлений"""
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter


class MyAdListAPIView(generics.ListAPIView):
    """Класс для просмотра списка объявлений пользователя"""
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = CustomPagination

    def get_queryset(self):
        """Метод для отображение только объявлений пользователя"""
        return Ad.objects.filter(author=self.request.user)


class AdRetrieveAPIView(generics.RetrieveAPIView):
    """Класс для просмотра объявления"""
    serializer_class = AdDetailSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated]


class AdUpdateAPIView(generics.UpdateAPIView):
    """Класс для изменения объявления"""
    serializer_class = AdDetailSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsAdmin]


class AdDestroyAPIView(generics.DestroyAPIView):
    """Класс для удаления объявления"""
    serializer_class = AdDetailSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsAdmin]


class CommentCreateAPIView(generics.CreateAPIView):
    """Класс для создания отзыва"""
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Метод для автоматической привязки отзыва к создателю и объявлению"""
        ad_pk = self.kwargs.get('ad_pk')
        ad_for_comment = Ad.objects.get(pk=ad_pk)
        comment_pk = self.kwargs.get('pk')
        serializer.save(author=self.request.user, ad=ad_for_comment, pk=comment_pk)


class CommentListAPIView(generics.ListAPIView):
    """Класс для просмотра списка отзывов"""
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс для просмотра, изменения и удаления отзыва"""
    lookup_field = 'comment_pk'
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, ad_pk, comment_pk):
        """Метод для получения отзыва"""
        try:
            comment = Comment.objects.get(ad_id=ad_pk, id=comment_pk)
            return Response({'comment': comment.text}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, ad_pk, comment_pk, *args, **kwargs):
        """Метод для изменения отзыва"""
        partial = kwargs.pop('partial', False)
        comment = Comment.objects.get(ad_id=ad_pk, id=comment_pk)
        if self.request.user == comment.author or self.request.user.groups.filter(name="Admin").exists():
            serializer = self.get_serializer(comment, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'message': 'Отзыв успешно изменен'})
        return Response({'message': 'У вас нет прав на изменение отзыва'})

    def destroy(self, request, ad_pk, comment_pk, *args, **kwargs):
        """Метод для удаления отзыва"""
        comment = Comment.objects.get(ad_id=ad_pk, id=comment_pk)
        if self.request.user == comment.author or self.request.user.groups.filter(name="Admin").exists():
            self.perform_destroy(comment)
            return Response({'message': 'Отзыв успешно удален'})
        return Response({'message': 'У вас нет прав на удаление отзыва'})
