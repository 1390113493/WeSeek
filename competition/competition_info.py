# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 0:22
# @Author  : HUII
# @FileName: competition_info.py
# @Software: PyCharm
import math

from competition.models import CompetitionInfo, CompetitionCollection


def get_info_list(page=1, limit=10, category=0):
    """
    获得比赛信息列表
    :param page:
    :param limit:
    :param category:
    :return:
    """
    if category:
        c_list = CompetitionInfo.objects.filter(category_id=category).order_by('-id').order_by('-deliver_date')
    else:
        c_list = CompetitionInfo.objects.all().order_by('-id').order_by('-deliver_date')
    count = c_list.count()
    max_page = math.ceil(count / limit)
    co_list = c_list[(page - 1) * limit: page * limit]
    info_list = []
    for info in co_list:
        info_list.append({
            'id': info.id,
            'title': info.title,
            'image': info.image,
            'time': info.deliver_date,
            'visit': info.visit,
            'collect': CompetitionCollection.objects.filter(competition_id=info.id, delete_time__isnull=True).count()
        })
    return {
        'amount': count,
        'max_page': max_page if max_page else 1,
        'list': info_list,
    }


def get_info_detail(c_id):
    """
    获得比赛详细信息
    :param c_id:
    :return:
    """
    competition = CompetitionInfo.objects.get(id=c_id)
    competition.visit = competition.visit + 1
    competition.save()
    return {
        'id': competition.id,
        'title': competition.title,
        'content': competition.content,
        'category': competition.category.name if competition.category else '',
        'host': competition.host,
        'visit': competition.visit,
        'time': competition.deliver_date,
        'image': competition.image,
        'collect': competition.competitioninfo.filter(delete_time__isnull=True).count()
    }

