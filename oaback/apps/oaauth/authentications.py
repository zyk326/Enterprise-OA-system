import jwt
import time
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
# from jwt.exceptions import ExpiredSignatureError
from apps.oaauth.models import OAUser


def generate_jwt(user):
    timestamp = time.time() + 60*60*24*7
    return jwt.encode({"userid":user.pk, "exp":timestamp}, settings.SECRET_KEY)

class UserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return request._request.user, request._request.auth

class JWTAuthentication(BaseAuthentication):
    keyword = "JWT"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = "不可用的JWT请求头!"
            raise AuthenticationFailed(msg)
        elif len(auth) == 2:
            msg = "不可用的JWT请求头,JWT Token中间不应该有空格!"
            raise AuthenticationFailed(msg)

        try:
            jwt_token = auth[1]
            jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
            userid = jwt_info["userid"]
            try:
                user = OAUser.objects.get(pk=userid)
                setattr(request, 'user', user)
                return user, jwt_token
            except:
                msg = "用户不存在!"
                raise AuthenticationFailed(msg)
        except:
            msg = "JWT Token已过期!"
            raise AuthenticationFailed(msg)
