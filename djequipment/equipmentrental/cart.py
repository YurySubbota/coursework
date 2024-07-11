from time import sleep
from datetime import datetime, timedelta
import pytz
from redis import Redis

CART_RESERVED_TIME = 3600


def reserved_until(seconds):
    tz_minsk = pytz.timezone('Europe/Minsk')
    datetime_minsk = datetime.now(tz_minsk)
    reserved_until_datetime = datetime_minsk + timedelta(seconds=seconds)
    reserved_until_time = reserved_until_datetime.strftime('%H:%M')
    return reserved_until_time


def use_redis():
    return Redis(host='localhost', port=6379, db=0)


def cart_add(key, value):
    return use_redis().setex(key, CART_RESERVED_TIME, value)


def cart_get(key):
    value = use_redis().get(key)
    if value is not None:
        value = value.decode('utf-8')
    reserved_seconds = use_redis().ttl(key)
    if reserved_seconds > 0:
        reserved = reserved_until(reserved_seconds)
    else:
        reserved = None
    return value, reserved


def is_reserved(key):
    if cart_get(key)[0] is None:
        return False
    else:
        return True


def users_cart(user_id):
    all_keys = use_redis().keys('*')
    equip_in_cart = []
    if not all_keys:
        return None
    for key in all_keys:
        if cart_get(key)[0] == user_id:
            equip_in_cart.append({'id': int(key.decode('utf-8')), 'time': cart_get(key)[1]})
    return equip_in_cart


def cart_remove(key):
    use_redis().delete(key)