from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from tire.serializers import UserTireInfoInputSerializer, UserTireInfoResponseSerializer


class UserTireSwaggerAutoSchema:
    create = dict(
        name="POST /user-tire_infos/",
        decorator=swagger_auto_schema(
            operation_id="사용자가 소유한 타이어 정보를 저장하는 API",
            operation_description="한 번에 최대 5명까지의 사용자에 대한 요청을 받을 수 있습니다.",
            request_body=UserTireInfoInputSerializer(many=True),
            responses={
                "200": UserTireInfoResponseSerializer(),
            },
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token {key}",
                                                 type=openapi.TYPE_STRING)]
        )
    )
