import asyncio, aiohttp
import datetime

from parse import parse
from django.core.validators import RegexValidator

from tire.models import Tire


async def _download_car_info(trim_id, item, timeout):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://dev.mycar.cardoc.co.kr/v1/trim/{trim_id}/', timeout=timeout) as resp:
                data = await resp.json()
                data[trim_id] = trim_id
                item.append(data)
                return data
        except asyncio.exceptions.TimeoutError:
            print("timeout")


def download_car_info_list(trim_ids):
    timeout = aiohttp.ClientTimeout(total=30)
    car_infos = []
    tasks = [_download_car_info(i, car_infos, timeout) for i in trim_ids]
    asyncio.run(asyncio.wait(tasks))
    return car_infos


def get_tire_from_car_info(car_info):
    front = car_info['spec']['driving']['frontTire']['value']
    rear = car_info['spec']['driving']['rearTire']['value']
    validate_tire_value_from_car_info(front)
    validate_tire_value_from_car_info(rear)
    front = parse('{f_width}/{f_profile}R{f_diameter}', front).named
    rear = parse('{r_width}/{r_profile}R{r_diameter}', rear).named
    tire = Tire(trim_id=car_info['trimId'], updated_at=datetime.datetime.now(), **front, **rear)
    return tire


def validate_tire_value_from_car_info(value):
    validator = RegexValidator(r'[0-9]{3}/[0-9]{2}R[0-9]{2}', 'tire value format invalid')
    validator(value)
