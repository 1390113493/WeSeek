# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 20:14
# @Author  : HUII
# @FileName: activities.py
# @Software: PyCharm
import datetime
import math

from activity.models import Activity, ActivityCollection


def get_activity_list(page=1, limit=10):
    """
    获得活动列表
    :param page:
    :param limit:
    :return:
    """
    a_list = Activity.objects.all().order_by('-id')
    count = a_list.count()
    max_page = math.ceil(count / limit)
    ac_list = a_list[(page - 1) * limit: page * limit]
    info_list = []
    for info in ac_list:
        info_list.append({
            'id': info.id,
            'title': info.title,
            'image': info.image,
            'time': str(info.from_time).split('.')[0] + ' ~ ' + str(info.to_time).split('.')[0],
            'visit': info.visit,
            'collect': ActivityCollection.objects.filter(activity_id=info.id, delete_time__isnull=True).count()
        })
    return {
        'amount': count,
        'max_page': max_page if max_page else 1,
        'list': info_list,
    }


def get_activity_detail(a_id):
    """
    获得活动内容
    :param a_id:
    :return:
    """
    activity = Activity.objects.get(id=a_id)
    Activity.objects.update(visit=activity.visit + 1)
    return {
        'id': activity.id,
        'title': activity.title,
        'content': activity.content,
        'host': activity.host,
        'visit': activity.visit,
        'time': str(activity.from_time).split('.')[0] + '~' + str(activity.to_time).split('.')[0],
        'image': activity.image,
        'collect': activity.activity.filter(delete_time__isnull=True).count()
    }


def add_activity(title, content, host, from_time, to_time):
    """
    新增活动
    :param title:
    :param content:
    :param host:
    :param from_time:
    :param to_time:
    :return:
    """
    try:
        from_time = datetime.datetime.strptime(from_time, "%Y-%m-%d %H:%M")
        to_time = datetime.datetime.strptime(to_time, "%Y-%m-%d %H:%M")
        Activity.objects.create(title=title, content=content, host=host, from_time=from_time, to_time=to_time)
        return True
    except:
        return False