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
        fields='__all__'

class UserTireInfoSerializer(serializers.ModelSerializer):
    tire = TireSerializer()

    class Meta:
        model = UserTire
        fields = '__all__'


