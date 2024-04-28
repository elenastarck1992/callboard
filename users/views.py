from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ads.permissions import IsOwner
from users.models import User
from users.serializers import UserSerializer, UserRegisterSerializer


class UserRegister(generics.CreateAPIView):
    """Класс для регистрации пользователя"""
    serializer_class = UserRegisterSerializer

    def create(self, request):
        """Метод для хэширования пароля пользователя в БД"""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserRetrieve(generics.RetrieveAPIView):
    """Класс для просмотра пользователя"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class UserUpdate(generics.UpdateAPIView):
    """Класс для обновления пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class UserList(generics.ListAPIView):
    """Класс для просмотра списка пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
