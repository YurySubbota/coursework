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
            equip_in_cart.append({'id': key.decode('utf-8'), 'time': cart_get(key)[1]})
    return equip_in_cart


def test_cart():
    print('add', cart_add(30, 'this user'))
    print('add', cart_add(20, 'this user'))
    print('add', cart_add(25, 'this user'))
    print('add', cart_add(100, 'other'))
    keys = use_redis().keys('*')
    print('keys', keys)
    print('user"this user"', users_cart('this user'))
    if users_cart('this user'):
        for eq in users_cart('this user'):
            print('this user equip', eq['id'])
            print('this user delite', eq['time'])
    while True:
        sleep(1)
        for key in keys:
            key = key.decode('utf-8')
            print('key', key)
            print('get_key', cart_get(key))
            print('get_not_key', cart_get(31))
            print('is_reserved', is_reserved(key))
            print('is_reserved_not_key', is_reserved(32))


if __name__ == '__main__':
    test_cart()
    pass
