from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from unicodedata import category
from django.http.response import JsonResponse
from rest_framework.status import HTTP_403_FORBIDDEN
from apps.oaauth.models import OAUser
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse

class LoginCheckMiddleware(MiddlewareMixin):
    keyword = 'JWT'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.white_list = [reverse("oaauth:login"),  reverse("staff:active_view") ]


    def process_view(self, request, view_func, view_args, view_kwargs):
        # 如果返回None会正常执行其他所有代码
        # 如果返回一个HttpResponse对象,将不会执行试图以及后面的中间件代码
        if request.path in self.white_list or request.path.startswith(settings.MEDIA_URL):
            request.user = AnonymousUser()
            request.auth = None
            return None
        try:
            auth = get_authorization_header(request).split()
            print(auth)
            if not auth or auth[0].lower() != self.keyword.lower().encode():
                raise exceptions.ValidationError("请传入JWT!")

            if len(auth) == 1:
                msg = "不可用的JWT请求头!"
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = "不可用的JWT请求头,JWT Token中间不应该有空格!"
                raise exceptions.AuthenticationFailed(msg)

            try:
                jwt_token = auth[1]
                jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
                userid = jwt_info["userid"]
                try:
                    user = OAUser.objects.get(pk=userid)
                    request.user = user
                    request.auth = jwt_token
                except:
                    msg = "用户不存在!"
                    raise exceptions.AuthenticationFailed(msg)
            except ExpiredSignatureError:
                msg = "JWT Token已过期!"
                raise exceptions.AuthenticationFailed(msg)
        except Exception as e:
            print(e)
            return JsonResponse(data={"detail":"请先登录!"}, status=HTTP_403_FORBIDDEN)