from django.contrib.auth.hashers import make_password
from user.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'password',
            'token',
        )

    def validate_password(self, value):
        return make_password(value)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        Token.objects.create(user=user)
        return user

    def get_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token
