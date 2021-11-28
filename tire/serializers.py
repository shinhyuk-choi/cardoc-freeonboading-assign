from rest_framework import serializers

from tire.models import UserTire, Tire


class UserTireInfoInputSerializer(serializers.Serializer):
    id = serializers.CharField()
    trimId = serializers.IntegerField()

    def validate(self, data):
        return super(UserTireInfoInputSerializer, self).validate(data)


class TireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tire
        exclude = (
            'id',
            'created_at',
            'updated_at',
        )


class UserTireInfoSerializer(serializers.ModelSerializer):
    tire = TireSerializer()

    class Meta:
        model = UserTire
        exclude = (
            'id',
            'created_at',
            'updated_at',
            'user',
        )


class UserTireInfoResponseSerializer(serializers.Serializer):
    count_create_tire = serializers.IntegerField()
    count_update_tire = serializers.IntegerField()
    count_create_user_tire_infos = serializers.IntegerField()
