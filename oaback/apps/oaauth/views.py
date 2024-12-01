from rest_framework import status
from rest_framework.views import APIView
from apps.oaauth.serializers import LoginSerializer, UserSerializer
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import ResetPwdSerializer
from rest_framework import status


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = datetime.now()
            user.save()
            token = generate_jwt(user)
            print(token)
            return Response({'token': token, 'user': UserSerializer(user).data})
        else:
            detail = list(serializer.errors.values())[0][0]
            print(serializer.errors)
            return Response({"detail":detail}, status=status.HTTP_400_BAD_REQUEST)

# class AuthenticatedRequierdView:
#     permission_classes = [permissions.IsAuthenticated]

class ResetPwdView(APIView):
    def post(self, request):
        serializer = ResetPwdSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pwd1 = serializer.validated_data.get('pwd1')
            request.user.set_password(pwd1)
            request.user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            detail = list(serializer.errors.values())[0][0]