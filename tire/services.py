# 서비스 계층
# 데이터베이스에서 데이터를 얻는다
# 도메인 모델을 업데이트 한다
# 변경된 내용을 역속화한다.
from django.db import transaction
from tire.logics import download_car_info_list, get_tire_from_car_info
from tire.models import Tire, UserTire, DataUserTire
from user.models import User


class TireService:
    @staticmethod
    def bulk_update_and_bulk_create_tire(data):
        trim_ids = [item['trimId'] for item in data]
        car_infos = download_car_info_list(trim_ids)
        tires = []
        for i in car_infos:
            tires.append(get_tire_from_car_info(i))
        with transaction.atomic():
            for_update = Tire.objects.filter(trim_id__in=trim_ids).values('id', 'trim_id')
            tire_for_update = []
            tire_for_create = []
            for tire in tires:
                flag = True
                for i in for_update:
                    if tire.trim_id == i['trim_id']:
                        tire.id = i['id']
                        tire_for_update.append(tire)
                        flag = False
                if flag:
                    tire_for_create.append(tire)

            Tire.objects.bulk_create(tire_for_create)
            # Tire.objects.bulk_update()


class UserTireInfoService:
    @staticmethod
    def bulk_create_user_tire_info(data):
        user_ids = [i['id'] for i in data]
        if User.objects.filter(id__in=user_ids).count() != len(data):
            raise User.DoesNotExist()
        if Tire.objects.filter(trim_id__in=[i['trimId'] for i in data]).count() != len(data):
            raise User.DoesNotExist()
        with transaction.atomic():
            data_user_tire_infos = set([DataUserTire(user_id=i['id'], tire_trim_id=i['trimId']) for i in data])
            tire_infos_from_db = list(UserTire.objects.filter(user_id__in=user_ids).values('user_id', 'tire_trim_id'))
            data_user_tire_infos_from_db = set([DataUserTire(**i) for i in tire_infos_from_db])
            data_user_tire_infos_for_create = [UserTire(**i.__dict__) for i in list(data_user_tire_infos - data_user_tire_infos_from_db)]
            UserTire.objects.bulk_create(data_user_tire_infos_for_create)
