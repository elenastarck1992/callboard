from django.urls import path

from ads.apps import AdsConfig
from ads.views import CommentRetrieveUpdateDestroyAPIView, AdListAPIView, AdCreateAPIView, MyAdListAPIView, \
    AdRetrieveAPIView, CommentCreateAPIView, CommentListAPIView, AdUpdateAPIView, AdDestroyAPIView

app_name = AdsConfig.name

urlpatterns = [
    path('', AdListAPIView.as_view(), name='ad-list'),
    path('create/', AdCreateAPIView.as_view(), name='ad-create'),
    path('me/', MyAdListAPIView.as_view(), name='ad-mylist'),
    path('<int:pk>/', AdRetrieveAPIView.as_view(), name='ad-detail'),
    path('<int:pk>/update/', AdUpdateAPIView.as_view(), name='ad-update'),
    path('<int:pk>/delete/', AdDestroyAPIView.as_view(), name='ad-delete'),
    path('<int:ad_pk>/comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('<int:ad_pk>/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('<int:ad_pk>/comments/<int:comment_pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(),
         name='comment-detail'),

]
