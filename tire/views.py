from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from swagger.tire import UserTireSwaggerAutoSchema
from tire.models import UserTire
from tire.serializers import UserTireInfoInputSerializer, UserTireInfoResponseSerializer

from tire.services import TireService, UserTireInfoService


class UserTireViewSet(viewsets.GenericViewSet):
    queryset = UserTire.objects.all()
    # serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @method_decorator(**UserTireSwaggerAutoSchema.create)
    def create(self, request):
        # Validation
        serializer = UserTireInfoInputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        if 0 < len(serializer.data) <= 5:
            data = serializer.data
        else:
            raise ValidationError('입력 body data형식이 유효하지 않습니다.')

        count_create_tire, count_update_tire = TireService.bulk_update_and_bulk_create_tire(data)
        count_create_user_tire_infos = UserTireInfoService.bulk_create_user_tire_info(data)
        return Response(UserTireInfoResponseSerializer(
            dict(count_create_tire=count_create_tire,
                 count_update_tire=count_update_tire,
                 count_create_user_tire_infos=count_create_user_tire_infos)
        ).data)
