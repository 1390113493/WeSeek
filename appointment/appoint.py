# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 23:13
# @Author  : HUII
# @FileName: appoint.py
# @Software: PyCharm
import datetime

from appointment.models import Appointment
from message.message import MessageManagement
from user.models import User


def add_appointment(uid, amount, from_time, to_time, remarks, phone, name, title, content):
    """
    新增预约
    :param uid: 预约人id
    :param amount: 人数
    :param from_time: 开始时间
    :param to_time: 结束时间
    :param remarks: 备注
    :param phone: 手机号
    :return:
    """
    try:
        from_time = datetime.datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S")
        to_time = datetime.datetime.strptime(to_time, "%Y-%m-%d %H:%M:%S")
        Appointment.objects.create(appointment_user_id=uid, amount=amount, from_time=from_time, to_time=to_time,
                                   remarks=remarks, phone=phone, name=name, title=title, content=content)
        MessageManagement(uid).send(
            title='申请加入队伍请求已发出',
            content=f'{User.objects.get(id=uid).name},你好！\n你申请预约的信息已提交到系统！。\n以下是您申请的信息：\n时间：{str(from_time).split(" ")[0]}~{str(to_time).split(" ")[0]}\n人数：{amount}\n联系人：{name}\n联系方式：{phone}\n请耐心等待系统管理员审核。我们将会根据实际情况确定您的预约信息，并将直接与您联系！\n感谢对WeSeek的支持！\n{str(datetime.datetime.now()).split(" ")[0]}'
        )
        return True
    except:
        return False


def cancel_appointment(uid, aid):
    """
    取消预约
    :param uid: 用户id
    :param aid: 预约id
    :return:
    """
    try:
        Appointment.objects.filter(appointment_user_id=uid, id=aid, delete_time__isnull=True).update(
            delete_time=datetime.datetime.now())
        MessageManagement(uid).send('成功取消预约', '您已成功取消了预约！感谢您的支持！')
        return True
    except:
        return False


def get_appointments(uid):
    """
    获得所有预约信息
    :param uid:
    :return:
    """
    appointments = Appointment.objects.filter(appointment_user_id=uid, delete_time__isnull=True)
    a_list = []
    for appointment in appointments:
        a_list.append({
            'id': appointment.id,
            'time': str(appointment.from_time).split('.')[0] + ' ~ ' + str(appointment.to_time).split('.')[0],
            'amount': appointment.amount,
            'remarks': appointment.remarks,
            'status': appointment.status,
            'response': appointment.response,
            'create_time': str(appointment.create_time).split('.')[0]
        })
    return a_list


def allow_appointment(aid, response):
    """
    允许预约申请
    :param aid:
    :param response:
    :return:
    """
    appoint = Appointment.objects.get(id=aid)
    appoint.status = True
    appoint.response = response
    appoint.save()
    MessageManagement(appoint.appointment_user.id).send(
        title='预约申请已通过',
        content=f'{appoint.appointment_user.name},你好！\n你的预约申请已通过！。\n{response}\n以下是您申请的信息：\n时间：{str(appoint.from_time).split(" ")[0]}~{str(appoint.to_time).split(" ")[0]}\n人数：{appoint.amount}\n联系人：{appoint.name}\n联系方式：{appoint.phone}\n请耐心等待系统管理员审核。我们将会根据实际情况确定您的预约信息，并将直接与您联系！\n感谢对WeSeek的支持！\n{str(datetime.datetime.now()).split(" ")[0]}'
    )
