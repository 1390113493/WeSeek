import jwt
import datetime
from jwt import exceptions
from WeSeek import settings

JWT_SALT = settings.SECRET_KEY


def create_token(payload, timeout=30):
    """
    创建token
    :param payload:  用户信息
    :param timeout: token的过期时间，默认1年（365天）
    :return:
    """
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=timeout)
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return result


def parse_payload(token):
    """
    对token进行和发行校验并获取payload
    :param token:
    :return:
    """
    result = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        verified_payload = jwt.decode(token, JWT_SALT, True)
        result['msg'] = 'token有效，获得用户信息成功'
        result['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        result['code'] = -1
        result['msg'] = 'token已过期失效'
    except jwt.DecodeError:
        result['code'] = -1
        result['msg'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['code'] = -1
        result['msg'] = '非法的token'
    return result


if __name__ == '__main__':
    print(parse_payload("eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NywiZXhwIjoxNjQ1NDIyMTA2fQ.fTvW4nbmlh3g2e7ykV82132lRfNwJ65SfK9ELPN8oyM"))