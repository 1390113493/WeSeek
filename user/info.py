# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 14:25
# @Author  : HUII
# @FileName: info.py
# @Software: PyCharm
from user.models import User


def get_user_info(uid):
    """
    获得用户信息
    :param uid:
    :return:
    """
    user = User.objects.get(id=uid)
    return {
        'id': user.id,
        'name': user.name,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'phone': user.username,
        'email': user.email,
        'gender': user.gender,
        'school': user.school,
        'major': user.major,
        'grade': user.grade,
        'stuid': user.stuid,
        'describe': user.describe,
        'join_time': str(user.create_time).split('.')[0]
    }


def set_user_info(uid, request_data):
    """
    设置用户信息
    :param uid:
    :param request_data:
    :return:
    """
    request_data = dict(request_data)
    for k, v in request_data.items():
        request_data[k] = v[0]
    try:
        User.objects.filter(id=uid).update(**request_data)
        return True
    except:
        return False