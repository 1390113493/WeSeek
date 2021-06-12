from django.db import models


# Create your models here.
class Activity(models.Model):
    """
    活动
    """
    title = models.CharField(verbose_name='标题', max_length=128, default='')
    content = models.TextField(verbose_name='内容', default='')
    visit = models.IntegerField(verbose_name='浏览量', default=0)
    host = models.CharField(verbose_name='主办方', max_length=32)
    image = models.CharField(verbose_name='图片', max_length=256, null=True, default=None)
    from_time = models.DateTimeField(verbose_name='开始时间')
    to_time = models.DateTimeField(verbose_name='结束时间')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    delete_time = models.DateTimeField(verbose_name='删除时间', null=True, default=None)


class ActivityCollection(models.Model):
    """
    收藏活动
    """
    a_collect_user = models.ForeignKey(verbose_name='收藏人', to='user.User', db_column='a_collect_user', related_name='a_collect_user', on_delete=models.Case)
    activity = models.ForeignKey(verbose_name='活动收藏', to='Activity', db_column='activity', related_name='activity', on_delete=models.Case)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    delete_time = models.DateTimeField(verbose_name='删除时间', null=True, default=None)

