import random
from app import *


def randomstring(num):
    items = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~!@#$%^&*(),.?[]{}-=+;:|'
    salt = ''
    for i in range(num):
        salt += random.choice(items)
    return salt


def check_password(input_str, store_str):
    length = len(store_str) - 8
    actual_p = store_str[2:length]
    if not input_str == actual_p[::-1]:
        return false
    return true
