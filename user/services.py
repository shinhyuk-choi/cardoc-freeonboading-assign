from tire.models import UserTire


class UserService:
    @staticmethod
    def get_user_tire_infos(user):
        return UserTire.objects.filter(user=user).select_related('user', 'tire')
