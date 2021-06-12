from django.db import models


class Category(models.Model):
    """
    比赛分类
    """
    name = models.CharField(verbose_name='名称', max_length=32)
    en_name = models.CharField(verbose_name='英文名', max_length=64)
    image = models.CharField(verbose_name='图片', max_length=256)
    describe = models.CharField(verbose_name='描述', max_length=2048)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '比赛分类'
        verbose_name_plural = verbose_name


class CompetitionInfo(models.Model):
    """
    比赛信息
    """
    title = models.CharField(verbose_name='标题', max_length=128)
    host = models.CharField(verbose_name='主办方', max_length=32)
    deliver_date = models.CharField(verbose_name='发布时间', max_length=20, null=True)
    category = models.ForeignKey(verbose_name='分类', to='Category', db_column='category', related_name='category',
                                 on_delete=models.Case, null=True, default=None)
    image = models.CharField(verbose_name='图片', max_length=256, null=True, default=None)
    describe = models.CharField(verbose_name='描述', max_length=2048, null=True, default=None)
    content = models.TextField(verbose_name='内容')
    visit = models.IntegerField(verbose_name='浏览量', default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '比赛信息'
        verbose_name_plural = verbose_name


class CompetitionCollection(models.Model):
    """
    收藏比赛
    """
    c_collect_user = models.ForeignKey(verbose_name='收藏人', to='user.User', db_column='c_collect_user',
                                       related_name='c_collect_user', on_delete=models.Case)
    competition = models.ForeignKey(verbose_name='活动', to='CompetitionInfo', db_column='competitioninfo',
                                    related_name='competitioninfo', on_delete=models.Case)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    delete_time = models.DateTimeField(verbose_name='删除时间', null=True, default=None)
