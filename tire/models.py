from dataclasses import dataclass

from django.db import models


class NamedForeignKey(models.ForeignKey):
    suffix_idname = 'id'

    def __init__(self, *args, **kwargs):
        suffix_idname = kwargs.pop('suffix_idname', None)
        if suffix_idname:
            self.suffix_idname = suffix_idname
        super().__init__(*args, **kwargs)

    def get_attname(self):
        return '%s_%s' % (self.name, self.suffix_idname)


class Tire(models.Model):
    class Meta:
        db_table = 'tire'

    trim_id = models.IntegerField(help_text="자동차 정보 조회 API의 trimId", unique=True)
    f_width = models.CharField(max_length=10, help_text="앞바퀴 단면폭")
    f_profile = models.CharField(max_length=10, help_text="앞바퀴 편평비")
    f_diameter = models.CharField(max_length=10, help_text="앞바퀴 림직경")
    r_width = models.CharField(max_length=10, help_text="뒷바퀴 단면폭")
    r_profile = models.CharField(max_length=10, help_text="뒷바퀴 편평비")
    r_diameter = models.CharField(max_length=10, help_text="뒷바퀴 림직경")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserTire(models.Model):
    class Meta:
        db_table = 'user_tire_info'

    user = models.ForeignKey(
        'user.User',
        to_field='id',
        on_delete=models.CASCADE,
        related_name="user_tires"
    )
    tire = NamedForeignKey(
        'tire.Tire',
        to_field='trim_id',
        suffix_idname='trim_id',
        db_column='tire_trim_id',
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_tires"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@dataclass(frozen=True)
class DataUserTire:
    user_id: str
    tire_trim_id: int
