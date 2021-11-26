from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError

from swagger.user import swagger_get_user_tire_infos
from tire.models import UserTire
from tire.serializers import UserTireInfoSerializer
from user.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from user.serializers import UserSerializer
from user.services import UserService


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated()]

    def get_permissions(self):
        if self.action in ('create', 'login'):
            return [AllowAny()]
        return self.permission_classes

    def create(self, request):
        """
        POST /users/

        data params
        - id(required)
        - password(required)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError:
            return Response({"error": "A user with that id already exists."}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        # response data
        data = serializer.data
        data['token'] = user.auth_token.key
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        POST /users/login/

        data params
        - id(required)
        - password(required)
        """
        username = request.data.get('id')
        password = request.data.get('password')

        user = authenticate(request, id=id, password=password)
        if user:
            login(request, user)

            data = self.get_serializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            return Response(data)
        return Response({"error": "Wrong username or wrong password"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        """
        POST /users/logout/
        """
        logout(request)
        return Response()

    @swagger_get_user_tire_infos
    @action(detail=True, methods=['GET'], url_path='user-tire-infos')
    def list_user_tire_infos(self, request, pk):
        if pk != "me":
            pass
        user_tire_infos = UserService.get_user_tire_infos(request.user)
        return Response(UserTireInfoSerializer(user_tire_infos, many=True).data)
