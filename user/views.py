from rest_framework.views import APIView, Response
from django.contrib.auth import authenticate, login, models

from extensions.jwt_auth import create_token
from extensions.response import fail, success
from user.home import user_home
from user.info import set_user_info, get_user_info
from user.models import User


class RegisterView(APIView):
    """
    用户注册视图
    """
    authentication_classes = []

    def post(self, *args, **kwargs):
        phone = self.request.POST.get('phone')
        password = self.request.POST.get('password')
        nickname = self.request.POST.get('nickname')
        if len(phone) != 11:
            return fail('手机号长度不正确')
        if len(password) < 6:
            return fail('密码长度不得小于6位')
        if not nickname:
            return fail('昵称不得为空')
        if User.objects.filter(username=phone):
            return fail('手机号已存在')
        if User.objects.filter(nickname=nickname):
            return fail('昵称已存在')
        User.objects.create_user(username=phone, password=password, nickname=nickname)
        return success('注册成功')


class LoginView(APIView):
    """
    登录视图
    """
    authentication_classes = []

    def post(self, *args, **kwargs):
        phone = self.request.POST.get('phone')
        password = self.request.POST.get('password')
        user = authenticate(username=phone, password=password)
        if user:
            token = create_token({
                'id': user.id
            }, timeout=7)
            return success(
                '登录成功',
                {
                    'token': token
                }
            )
        else:
            return fail('用户名或密码错误')


class UserInfoView(APIView):
    """
    用户信息视图
    """
    def get(self, *args, **kwargs):
        uid = self.request.user
        return success('成功获得用户信息', get_user_info(uid))

    def post(self, *args, **kwargs):
        uid = self.request.user
        if set_user_info(uid, self.request.POST):
            return success('成功设置用户信息')
        else:
            return fail('设置用户信息失败')


class CommonUserInfo(APIView):
    """
    获得其他用户信息接口
    """
    authentication_classes = []

    def get(self, *args, **kwargs):
        uid = self.request.GET.get('uid')
        return success('成功获得用户信息', get_user_info(uid))

class HomeView(APIView):
    """
    用户中心
    """
    def get(self, *a, **kwargs):
        uid = self.request.user
        return success('成功获得用户中心信息', user_home(uid))


class TestView(APIView):
    def get(self, *args, **kwargs):
        self.request.data
        return success('成功了')