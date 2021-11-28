from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body

from tire.serializers import UserTireInfoSerializer
from user.serializers import UserSerializer


class UserSwaggerAutoSchema:
    create = dict(
        name="POST /users/",
        decorator=swagger_auto_schema(
            operation_id="사용자 생성",
            operation_description="Response에 password는 노출되지 않습니다",
            responses={
                "200": UserSerializer(),
            }
        )
    )

    login = dict(
        name="POST /users/login/",
        decorator=swagger_auto_schema(
            operation_id="사용자 로그인",
            operation_description="Response에 password는 노출되지 않습니다",
            responses={
                "200": UserSerializer(),
            }
        )
    )

    logout = dict(
        name="POST /users/logout/",
        decorator=swagger_auto_schema(
            operation_id="사용자 로그아웃",
            operation_description="",
            request_body=no_body,
            responses={
                "200": "",
            }
        )
    )

    list_user_tire_infos = dict(
        name="GET /users/me/user-tire-infos/",
        decorator=swagger_auto_schema(
            operation_id="사용자가 소유한 타이어 정보 조회",
            operation_description="""
            로그인한 사용자의 타이어 정보 리스트
            """,
            responses={
                "200": UserTireInfoSerializer(many=True),
            },
            manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token {key}",
                                                 type=openapi.TYPE_STRING)]
        )
    )
