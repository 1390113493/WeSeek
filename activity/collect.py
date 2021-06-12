# -*- coding: utf-8 -*-
# @Time    : 2021/6/8 22:31
# @Author  : HUII
# @FileName: collect.py
# @Software: PyCharm
from activity.models import ActivityCollection


def status(uid, cid):
    """
    收藏状态
    :param uid: 用户id
    :param cid: 比赛id
    :return:
    """
    if ActivityCollection.objects.filter(a_collect_user_id=uid, activity_id=cid):
        return True
    else:
        return False


def deal(uid, cid):
    """
    处理收藏请求
    :param uid:
    :param cid:
    :return:
    """
    if status(uid, cid):
        ActivityCollection.objects.filter(a_collect_user_id=uid, activity_id=cid).delete()
        return '取消收藏成功'
    else:
        ActivityCollection.objects.create(a_collect_user_id=uid, activity_id=cid)
        return '收藏成功'


def collect_list(uid):
    """
    活动收藏列表
    :param uid:
    :return:
    """
    collects = ActivityCollection.objects.filter(a_collect_user_id=uid)
    collect_ls = []
    for collect in collects:
        activity = collect.activity
        collect_ls.append({
            'id': activity.id,
            'title': activity.title,
            'content': activity.content,
            'host': activity.host,
            'time': str(activity.from_time).split('.')[0] + '~' + str(activity.to_time).split('.')[0],
            'image': activity.image,
        })
    return collect_ls
