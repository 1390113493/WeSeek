from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    用户表
    """
    gender_choice = (
        ("2", "未知"),
        ("1", "男"),
        ('0', "女"),
    )
    name = models.CharField(verbose_name='真实姓名', max_length=32)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    school = models.CharField(verbose_name='学校', max_length=32)
    stuid = models.CharField(verbose_name='学号', max_length=32)
    major = models.CharField(verbose_name='专业', max_length=32)
    grade = models.CharField(verbose_name='年级', max_length=32)
    describe = models.CharField(verbose_name='自我描述', max_length=1024)
    email = models.EmailField(verbose_name='邮箱', max_length=255, null=True, blank=True)
    # phone = models.CharField(verbose_name="手机号码", max_length=50, unique=True)
    avatar = models.URLField(verbose_name="用户头像", default="")
    gender = models.CharField(verbose_name='性别', max_length=4, choices=gender_choice, default="未知")
    create_time = models.DateTimeField(verbose_name="注册时间", auto_now_add=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username[0].upper()


class LoginRecord(models.Model):
    """
    登录记录
    """
    uid = models.ForeignKey(verbose_name='用户id', to='User', related_name='uid', db_column='uid', on_delete=models.Case)
    login_time = models.DateTimeField(verbose_name="登录时间", auto_now=True)
    ip = models.GenericIPAddressField(verbose_name="访问IP", default="0.0.0.0")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '登录记录'
        verbose_name_plural = verbose_name
