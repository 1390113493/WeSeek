from django.db import models


class Message(models.Model):
    """
    消息推送，包括有人请求加入，请求加入成功，请求加入被拒绝，
    """
    from_user = models.ForeignKey(verbose_name='发送消息用户(空表示系统)', to='user.User', related_name='from_user', db_column='from_user',
                                on_delete=models.Case, null=True, default=None)
    to_user = models.ForeignKey(verbose_name='接收消息用户', to='user.User', related_name='to_user', db_column='to_user',
                                on_delete=models.Case)
    message_title = models.CharField(verbose_name='消息标题', max_length=32, null=True, default=None)
    message_content = models.CharField(verbose_name='消息内容', max_length=1024)
    have_read = models.BooleanField(verbose_name='是否已读', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '加入队伍'
        verbose_name_plural = verbose_name

