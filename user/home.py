from activity.collect import collect_list as a_collect_list
from appointment.models import Appointment
from competition.collect import collect_list as c_collect_list
from group.models import Join, InitialiseGroup
from user.info import get_user_info


def user_home(uid):
    """
    用户中心
    :param uid:
    :return:
    """
    return {
        'competition': get_user_join_group(uid),
        'appointment': get_user_appointment(uid),
        'collect': get_collection(uid),
        'group': get_group_and_join_users(uid)
    }


def get_user_join_group(uid):
    """
    获得该用户申请加入的队伍
    :param uid:
    :return:
    """
    joins = Join.objects.filter(member_id=uid)
    join_list = []
    for join in joins:
        join_list.append({
            'cid': join.group_id.competition_id,
            'gid': join.group_id_id,
            'title': join.group_id.competition.title,
            'level': '省级',
            'host': join.group_id.competition.host,
            'deadline': join.group_id.allow_time,
            'status': '被拒绝' if join.refused else '已同意' if join.allowed_time else '未审核',
            # 'refused': join.group_id.refused,
            'apply_time': str(join.join_time).split('.')[0],
            'allowd_time': str(join.allowed_time).split('.')[0],
            'user': get_user_info(join.group_id.initiator_id)
        })
    return join_list


def get_user_appointment(uid):
    """
    获得该用户申请的预约
    :param uid:
    :return:
    """
    appointments = Appointment.objects.filter(appointment_user_id=uid)
    applontment_list = []
    for appointment in appointments:
        applontment_list.append({
            'aid': appointment.id,
            'from': str(appointment.from_time).split('.')[0],
            'to': str(appointment.to_time).split('.')[0],
            'title': appointment.title,
            'content': appointment.content,
            'amount': appointment.amount,
            'remarks': appointment.remarks,
            'status': '已处理' if appointment.status else '未处理',
            'response': appointment.response,
            'name': appointment.name,
            'phone': appointment.phone
        })
    return applontment_list


def get_collection(uid):
    """
    获得用户的收藏
    :param uid:
    :return:
    """
    a_collect = a_collect_list(uid)
    c_collect = c_collect_list(uid)
    return {
        'competition': c_collect,
        'activity': a_collect
    }


def get_group_and_join_users(uid):
    """
    获得创建的队伍及其申请人
    :param uid:
    :return:
    """
    groups = InitialiseGroup.objects.filter(initiator_id=uid)
    group_list = []
    for group in groups:
        joins = Join.objects.filter(group_id=group.id)
        join_list = []
        for join in joins:
            join_list.append({
                'id': join.id,
                'refused': join.refused,
                'apply_time': str(join.join_time).split('.')[0],
                'allowed_time': str(join.join_time).split('.')[0],
                'user': get_user_info(join.member_id)
            })
        group_list.append({
            'gid': group.id,
            'amount': group.amount,
            'deadline': str(group.allow_time).split('.')[0],
            'join': join_list
        })
    return group_list