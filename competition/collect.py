# -*- coding: utf-8 -*-
# @Time    : 2021/6/8 22:31
# @Author  : HUII
# @FileName: collect.py
# @Software: PyCharm
from competition.models import CompetitionCollection


def status(uid, cid):
    """
    收藏状态
    :param uid: 用户id
    :param cid: 比赛id
    :return:
    """
    if CompetitionCollection.objects.filter(c_collect_user_id=uid, competition_id=cid):
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
        CompetitionCollection.objects.filter(c_collect_user_id=uid, competition_id=cid).delete()
        return '取消收藏成功'
    else:
        CompetitionCollection.objects.create(c_collect_user_id=uid, competition_id=cid)
        return '收藏成功'


def collect_list(uid):
    """
    活动收藏列表
    :param uid:
    :return:
    """
    collects = CompetitionCollection.objects.filter(c_collect_user_id=uid)
    collect_ls = []
    for collect in collects:
        info = collect.competition
        collect_ls.append({
            'id': info.id,
            'title': info.title,
            'image': info.image,
            'time': info.deliver_date
        })
    return collect_ls