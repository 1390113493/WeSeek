from django.db import models


# Create your models here.
class InitialiseGroup(models.Model):
    """
    新建组队
    """
    initiator = models.ForeignKey(verbose_name='发起人', to='user.User', related_name='initiator', db_column='initiator',
                                  on_delete=models.Case)
    amount = models.IntegerField(verbose_name='招募队员数量', default=5)
    competition = models.ForeignKey(verbose_name='比赛', to='competition.CompetitionInfo', related_name='competition',
                                    db_column='competition', on_delete=models.Case)
    requirement = models.TextField(verbose_name='期望队友要求', null=True, default=None)
    allow_time = models.DateTimeField(verbose_name='截止招募时间', null=True, default=None)
    remarks = models.TextField(verbose_name='备注', null=True, default=None)
    success = models.BooleanField(verbose_name='组队成功', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '新建组队'
        verbose_name_plural = verbose_name


class Join(models.Model):
    """
    加入队伍
    """
    group_id = models.ForeignKey(verbose_name='队伍', to='InitialiseGroup', related_name='group_id', db_column='group_id',
                                 on_delete=models.Case)
    member = models.ForeignKey(verbose_name='组员', to='user.User', related_name='member', db_column='member',
                               on_delete=models.Case)
    join_time = models.DateTimeField(verbose_name='请求加入时间', auto_now_add=True)
    allowed_time = models.DateTimeField(verbose_name='允许时间', blank=True, null=True)
    refused = models.BooleanField(verbose_name='是否被发起人拒绝', default=False)
    cancel = models.BooleanField(verbose_name='是否取消申请', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '加入队伍'
        verbose_name_plural = verbose_name




