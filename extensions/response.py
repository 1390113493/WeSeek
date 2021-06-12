# -*- coding: utf-8 -*-
# @Time    : 2021/5/26 0:09
# @Author  : HUII
# @FileName: response.py
# @Software: PyCharm
from rest_framework.views import Response


def success(message='success', data=None):
    """
    请求成功调用该接口
    :param message:
    :param data:
    :return:
    """
    if data != None:
        res = {
            'code': 0,
            'msg': message,
            'data': data
        }
    else:
        res = {
            'code': 0,
            'msg': message
        }
    return Response(res)


def fail(message='fail', data=None):
    """
    请求失败调用该接口
    :param message:
    :param data:
    :return:
    """
    if data != None:
        res = {
            'code': -1,
            'msg': message,
            'data': data
        }
    else:
        res = {
            'code': -1,
            'msg': message
        }
    return Response(res)
