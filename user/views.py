from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError

from swagger.user import UserSwaggerAutoSchema
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

    @method_decorator(**UserSwaggerAutoSchema.create)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError:
            return Response({"error": "A user with that id already exists."}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        data = serializer.data
        data['token'] = user.auth_token.key
        return Response(data, status=status.HTTP_201_CREATED)

    @method_decorator(**UserSwaggerAutoSchema.login)
    @action(detail=False, methods=['POST'])
    def login(self, request):
        login_id = request.data.get('id')
        password = request.data.get('password')

        user = authenticate(request, id=login_id, password=password)
        if user:
            login(request, user)

            data = self.get_serializer(user).data
            return Response(data)
        return Response({"error": "Wrong id or wrong password"}, status=status.HTTP_403_FORBIDDEN)

    @method_decorator(**UserSwaggerAutoSchema.logout)
    @action(detail=False, methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response()

    @method_decorator(**UserSwaggerAutoSchema.list_user_tire_infos)
    @action(methods=['GET'], url_path='me/user-tire-infos', detail=False)
    def list_user_tire_infos(self, request):
        user_tire_infos = UserService.get_user_tire_infos(request.user)
        return Response(UserTireInfoSerializer(user_tire_infos, many=True).data)
