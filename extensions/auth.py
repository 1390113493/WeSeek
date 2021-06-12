from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from user.models import User
from .jwt_auth import parse_payload


class JwtAuthorizationAuthentication(BaseAuthentication):
    """
    用户需要通过请求头的方式来进行传输token
    """
    def authenticate(self, request):
        # 非登录页面需要校验token
        token = request.META.get('HTTP_TOKEN', '')
        if not token:
            raise exceptions.AuthenticationFailed({
                'code': -1,
                'msg': '未在请求头中传token'
            })
        if len(token.split('.')) != 3:
            raise exceptions.AuthenticationFailed({
                'code': -1,
                'msg': '请求头格式错误'
            })

        result = parse_payload(token)
        if result['code'] != 200:
            del result['data']
            raise exceptions.AuthenticationFailed(result)
        if not User.objects.filter(id=result['data']['id']):
            raise exceptions.AuthenticationFailed({
                'code': -1,
                'msg': '非法的token'
            })
        # 如果想要request.user等于用户对象，此处可以根据payload去数据库中获取用户对象。
        return (result['data']['id'], token)
