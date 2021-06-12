from django.db.models import Q

from activity.models import Activity, ActivityCollection
from competition.models import CompetitionInfo, CompetitionCollection
from user.info import get_user_info
from user.models import User


def search(keyword):
    """
    搜索功能
    :param keyword:
    :return:
    """
    c_res = search_competition(keyword)
    a_res = search_activity(keyword)
    return {
        'competition': c_res,
        'activity': a_res
    }


def search_competition(keyword):
    """
    从比赛信息中搜索
    :param keyword:
    :return:
    """
    competitions = CompetitionInfo.objects.filter(Q(title__contains=keyword)|Q(content__contains=keyword))
    competition_list = []
    for info in competitions:
        competition_list.append({
            'id': info.id,
            'title': info.title,
            'image': info.image,
            'time': info.deliver_date,
            'visit': info.visit,
            'collect': CompetitionCollection.objects.filter(competition_id=info.id, delete_time__isnull=True).count()

        })
    return competition_list


def search_activity(keyword):
    """
    从活动中搜索
    :param keyword:
    :return:
    """
    activities = Activity.objects.filter(Q(title__contains=keyword)|Q(content__contains=keyword))
    activity_list = []
    for info in activities:
        activity_list.append({
            'id': info.id,
            'title': info.title,
            'image': info.image,
            'time': str(info.from_time) + ' ~ ' + str(info.to_time),
            'visit': info.visit,
            'collect': ActivityCollection.objects.filter(activity_id=info.id, delete_time__isnull=True).count()
        })
    return activity_list


def search_student(keyword):
    """
    搜索用户昵称
    :param keyword:
    :return:
    """
    users = User.objects.filter(nickname__icontains=keyword).values_list('id', flat=True)
    user_list = []
    for user in users:
        user_list.append(get_user_info(user))
    return user_list
