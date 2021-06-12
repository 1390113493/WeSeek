from django.db import models


class Appointment(models.Model):
    """
    预约
    """
    appointment_user = models.ForeignKey(verbose_name='预约人', to='user.User', db_column='appointment_user', related_name='appointment_user', on_delete=models.Case) 
    amount = models.IntegerField(verbose_name='预约人数')
    title = models.CharField(verbose_name='活动主题', max_length=64, null=True, default='')
    content = models.TextField(verbose_name='活动内容', null=True, default='')
    from_time = models.DateTimeField(verbose_name='预约开始时间')
    to_time = models.DateTimeField(verbose_name='预约结束时间')
    remarks = models.CharField(verbose_name='备注', max_length=512, null=True, default='')
    response = models.CharField(verbose_name='回复', max_length=512, default='')
    name = models.CharField(verbose_name='姓名', max_length=8, default='')
    phone = models.CharField(verbose_name='手机号', max_length=20, null=True, default=None)
    status = models.BooleanField(verbose_name='状态，False为还未成功', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    delete_time = models.DateTimeField(verbose_name='删除时间', null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '预约信息'
        verbose_name_plural = verbose_name
