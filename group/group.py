# -*- coding: utf-8 -*-
# @Time    : 2021/5/28 10:52
# @Author  : HUII
# @FileName: group.py
# @Software: PyCharm
import datetime

from competition.models import CompetitionInfo
from message.message import MessageManagement
from user.models import User
from .models import InitialiseGroup, Join


class Group:
    """
    组队
    """

    def __init__(self, uid, gid=0):
        self.uid = uid
        self.gid = gid
        self.user = User.objects.get(id=uid)
        self.day = str(datetime.datetime.now()).split(" ")[0]

    def check_user_info(func):
        """
        装饰器：检查用户信息，是否认证
        :return:
        """

        def check(self, *args, **kwargs):
            if not self.user.name:
                return False, '未绑定身份'
            return func(self, *args, **kwargs)

        return check

    def check_group_status(func):
        """
        装饰器：检查队伍状态
        :return:
        """

        def check(self, *args, **kwargs):
            group = InitialiseGroup.objects.get(id=self.gid)
            now = datetime.datetime.now()
            if group.allow_time < now:
                return False, '超过组队时间，该队伍已不再允许加入'
            return func(self, *args, **kwargs)

        return check

    @check_user_info
    def initialise_group(self, competition, amount, requirement, allow_time, remarks=''):
        """
        创建队伍
        :param allow_time: 最晚允许加入时间
        :param competition: 比赛id
        :param amount: 最多人数
        :param requirement: 要求
        :param remarks: 备注
        :return: 是否成功，message
        """
        if InitialiseGroup.objects.filter(initiator_id=self.uid, competition_id=competition):
            return False, '已创建其他队伍'
        else:
            allow_time = datetime.datetime.strptime(allow_time, "%Y-%m-%d %H:%M:%S")
            InitialiseGroup.objects.create(initiator_id=self.uid, amount=amount, competition_id=competition,
                                           requirement=requirement, allow_time=allow_time, remarks=remarks)
            MessageManagement(self.uid).send(
                title='创建队伍成功',
                content=f'{self.user.name},你好！\n你已成功创建了“{CompetitionInfo.objects.get(id=competition).title}”比赛的队伍。\n队伍的人数限制为{amount}人，队伍报名截止时间为{allow_time}。\n感谢对WeSeek的支持！\n{self.day}'
            )
            return True, '创建队伍成功'

    @check_user_info
    @check_group_status
    def join_group(self):
        """
        加入队伍
        :return: 是否成功，message
        """
        cid = InitialiseGroup.objects.get(id=self.gid).competition
        if InitialiseGroup.objects.filter(id=self.gid, initiator_id=self.uid):
            return False, '你是发起人，不需要再加入'
        if InitialiseGroup.objects.filter(competition_id=cid, initiator_id=self.uid):
            return False, '你已作为本比赛其他队伍的发起人，不允许再加入其他队伍'
        if Join.objects.filter(group_id_id=self.gid, member_id=self.uid, refused=False, cancel=False):
            return False, '你已申请加入该队，请耐心等待'
        if Join.objects.filter(group_id__competition=cid, member_id=self.uid, refused=False, cancel=False):
            return False, '你已经申请加入其他团队，撤回申请后才可申请加入本团队'
        else:
            Join.objects.create(group_id_id=self.gid, member_id=self.uid)
            MessageManagement(self.uid).send(
                title='申请加入队伍请求已发出',
                content=f'{self.user.name},你好！\n你申请加入{InitialiseGroup.objects.get(id=self.gid).initiator.username}的队伍请求已发出。\n请耐心等待该队伍发起人的同意。\n感谢对WeSeek的支持！\n{self.day}'
            )
            return True, '请求成功，请等待队伍发起人处理'

    @check_user_info
    def cancel_join(self):
        """
        撤回加入队伍申请
        :return:  是否成功，message
        """
        join = Join.objects.filter(group_id_id=self.gid, member_id=self.uid, refused=False, cancel=False)
        if join:
            join.update(refused=True)

            return True, '你已取消加入该队的申请'
        else:
            return False, '你未申请加入本队伍'

    def manage(self, jid, status):
        """
        对申请加入队伍的进行管理
        :param jid: 加入id
        :param status: 同意:1, 拒绝:0
        :return:
        """
        try:
            if status:
                Join.objects.filter(id=jid, group_id__initiator_id=self.uid).update(refused=False,
                                                                                    allowed_time=datetime.datetime.now())
                MessageManagement(self.uid).send(
                    title='加入队伍申请已被同意',
                    content=f'{self.user.name},你好！\n你申请加入{InitialiseGroup.objects.get(id=self.gid).initiator.username}的队伍请求已被发起人的同意。祝比赛取得好成绩！\n感谢对WeSeek的支持！\n{self.day}'
                )
            else:
                Join.objects.filter(id=jid, group_id__initiator_id=self.uid).update(refused=True, allowed_time=None)
                MessageManagement(self.uid).send(
                    title='加入队伍申请被拒绝',
                    content=f'{self.user.name},你好！\n你申请加入{InitialiseGroup.objects.get(id=self.gid).initiator.username}的队伍请求被发起人拒绝。你可以加入其他队伍！\n感谢对WeSeek的支持！\n{self.day}'
                )
            return True
        except:
            return False


def group_info(gid):
    """
    队伍信息
    :param gid: 队伍id
    :return:
    """
    group = InitialiseGroup.objects.get(id=gid)
    user = group.initiator
    return {
        'id': group.id,
        'amount': group.amount,
        'join_count': group.group_id.filter(allowed_time__isnull=False, refused=False, cancel=False).count(),
        'requirement': group.requirement,
        'remarks': group.remarks,
        'create_time': str(group.create_time),
        'allow_time': str(group.allow_time),
        'user': {
            'id': user.id,
            'name': user.name,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'gender': user.gender,
            'school': user.school,
            'major': user.major,
            'grade': user.grade
        }
    }


def group_list(cid):
    """
    队伍列表
    :param cid: 比赛id
    :return:
    """
    groups = InitialiseGroup.objects.filter(competition=cid)
    group_ls = []
    for group in groups:
        user = group.initiator
        group_ls.append({
            'id': group.id,
            'amount': group.amount,
            'join_count': group.group_id.filter(allowed_time__isnull=False, refused=False, cancel=False).count(),
            'nickname': user.nickname,
            'avatar': user.avatar,
        })
    return group_ls
