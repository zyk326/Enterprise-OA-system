from django.shortcuts import render
from kombu.resource import Resource
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from apps.oaauth.models import OADepartment, UserStatusChoices
from apps.oaauth.serializers import DepartmentSerializer, UserSerializer
from .serializers import AddStaffSerializer, OAUser, ActiveStaffSerializer, StaffUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from utils import aeser
from django.urls import reverse
from oaback.celery import debug_task
from .tasks import send_mail_task
from django.views import View
from django.http.response import JsonResponse
from urllib import parse
from rest_framework import generics, exceptions
from .paginations import StaffListPagination
from rest_framework import viewsets
from rest_framework import mixins
from datetime import datetime
import json
import pandas as pd
from django.http.response import HttpResponse
from django.db import transaction

aes = aeser.AESCipher(settings.SECRET_KEY)


def send_active_email(request, email):
    token = aes.encrypt(email)
    # staff/active?token=xxx 这里有一个编码的问题,+会被识别成空格.
    active_path = reverse('staff:active_view') + "?" + parse.urlencode({'token': token})
    # 构建绝对路由
    active_url = request.build_absolute_uri(active_path)
    message = f'请点击以下链接激活账号:{active_url}'
    subject = f'[OA系统]账号激活'
    # 发送一个链接,点击跳转到激活页面,才能激活.
    # 为了区分用户,在发送链接邮件需要包含用户的邮箱.
    # 针对邮箱进行AES加密.
    # send_mail(f'[OA系统]账号激活', recipient_list=[email], message=message, from_email=settings.DEFAULT_FROM_EMAIL)  # 这是同步代码
    send_mail_task.delay(email, subject, message)

# 回传结果是results
class DepartmentListView(ListAPIView):
    queryset = OADepartment.objects.all()
    serializer_class = DepartmentSerializer

# 把用户访问时的token存储在cookie中
# 校验用户上传的邮箱和密码,解密token,比对提交的邮箱与数据库中的
class ActiveStaffView(View):
    def get(self, request):
        # 获取token并存储,方便用户下次传过来
        # http://localhost:8000/staff/active?token=+QoDzE8b+vQI5r/0sm6xbJXd78YJfgAQvOdINLQnqKrT01JPDjpHnmMLS3NmC/u1
        token = request.GET.get('token')
        response = render(request, 'active.html')
        response.set_cookie('token', token)
        return response

    def post(self, request):
        # token的aes加密的email
        # django的request获取数据用request.POST
        # rest_framework的request获取数据用request.data
        try:
            token = request.COOKIES.get('token')
            print(token)
            email = aes.decrypt(token)
            print(email)
            print(request.POST)
            serializer = ActiveStaffSerializer(data=request.POST)
            if serializer.is_valid():
                form_email = serializer.validated_data.get('email')
                user = serializer.validated_data.get('user')
                if email != form_email:
                    return JsonResponse({'code':400, 'message':"邮箱错误!"})
                user.status = UserStatusChoices.ACTIVED
                user.save()
                return JsonResponse({"code":200})
            else:
                detail = list(serializer.errors.values())[0][0]
                return JsonResponse({'code': 400, 'message':detail})
        except Exception as e:
            return JsonResponse({'code':400, 'message':'token错误!'})


class StaffViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = OAUser.objects.all()
    # 自定一个分页逻辑
    pagination_class = StaffListPagination

    def get_serializer_class(self):
        if self.request.method in ['GET', 'PUT']:
            return UserSerializer
        else:
            return AddStaffSerializer

    # 获取员工列表
    def get_queryset(self):
        department_id = self.request.query_params.get('department_id')
        realname = self.request.query_params.get('realname')
        date_joined = self.request.query_params.getlist('date_joined[]')
        queryset = self.queryset
        # 如果是董事会的，返回所有员工
        # 如果不是董事会的，但是是部门leader，那么就返回部门的员工
        # 如果不是董事会的，也不是部门leader，那么就抛出403
        user = self.request.user
        if user.department.name != '董事会':
            if user.uid != user.department.leader.uid:
                raise exceptions.PermissionDenied()
            else:
                queryset = queryset.filter(department_id=user.department_id)
        else:
            # 董事会中根据部门id进行过滤
            if department_id:
                queryset = queryset.filter(department_id=department_id)

        if realname:
            queryset = queryset.filter(realname__icontains=realname)
        if date_joined:
            try:
                start_date = datetime.strptime(date_joined[0], '%Y-%m-%d')
                end_date = datetime.strptime(date_joined[-1], '%Y-%m-%d')
                queryset = queryset.filter(date_joined__range=(start_date, end_date))
            except Exception as e:
                pass
        return queryset.order_by('-date_joined').all()

    def update(self, request, *args, **kwargs):
        # 默认情况下,如果要修改某一条数据,要传入这个数据序列化中的所有字段
        # 如果只想修改一部分数据,那么可以在kwargs中设置partial为True
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    # 新增员工
    def create(self, request, *args, **kwargs):
        # 如果用的是视图集,会自动把request放入context中.
        serializer = AddStaffSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            realname = serializer.validated_data.get('realname')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = OAUser.objects.create_user(realname=realname, email=email, password=password)
            department = request.user.department
            user.department = department
            user.save()

            send_active_email(request, email)

            return Response()
        else:
            return Response(data={'detail': list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)


class StaffDownloadView(APIView):
    def get(self, request):
        # ['x', 'y'] => Json格式字符串
        pks = request.query_params.get('pks')
        try:
            pks = json.loads(pks)
        except Exception as e:
            return Response({'detail':"员工参数错误!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            current_user = request.user
            queryset = OAUser.objects
            if current_user.department.name != '董事会':
                if current_user.department.leader_id != current_user.uid:
                    return Response({'detail':'没有权限下载!'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    queryset.filter(department_id=current_user.department_id)
            queryset = queryset.filter(pk__in=pks)
            result = queryset.values('realname', 'email', 'department__name', 'date_joined', 'status')
            staff_df = pd.DataFrame(list(result))
            staff_df = staff_df.rename(columns={'realname':'姓名', 'email':'邮箱', 'department__name':'部门', 'date_joined':'入职日期', 'status':'状态'})
            response = HttpResponse(content_type='application/xlsx')
            response['Content-Disposition'] = 'attachment; filename="员工信息.xlsx"'
            # 把staff_df写入到response中
            with pd.ExcelWriter(response) as writer:
                staff_df.to_excel(writer, sheet_name='员工信息')
            return response
        except Exception as e:
            print(e)
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StaffUploadView(APIView):
    def post(self, request):
        serializer = StaffUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data.get('file')
            current_user = request.user
            if current_user.department.name != '董事会' or current_user.uid != current_user.department.leader.uid:
                return Response({'detail':'您没有权限访问!'}, status=status.HTTP_403_FORBIDDEN)
            staff_df = pd.read_excel(file)
            users = []
            for index, row in staff_df.iterrows():
                # 获取部门
                if current_user.department.name != '董事会':
                    department = current_user.department
                else:
                    try:
                        department = OADepartment.objects.filter(name=row['部门']).first()
                        if not department:
                            return Response({'detail':f"{row['部门']}不存在!"}, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        return Response({'detail':"部门列不存在!"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    email = row['邮箱']
                    realname = row['姓名']
                    password = '111111'
                    user = OAUser(email=email, realname=realname, department=department, status=UserStatusChoices.UNACTIVE)
                    user.set_password(password)
                    users.append(user)
                except Exception:
                    return Response({'detail':"请检查文件中邮箱,姓名,部门名称!"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                # 统一把数据添加到数据库中,原子操作(事务)
                with transaction.atomic():
                    OAUser.objects.bulk_create(users)
            except Exception:
                return Response({'detail':'员工数据添加错误!'}, status=status.HTTP_400_BAD_REQUEST)

            # 异步给每个新增员工发送邮件
            for user in users:
                send_active_email(request, user.email)
            return Response()
        else:
            detail = list(serializer.errors.values())[0][0]
            return Response({'detail':detail}, status=status.HTTP_400_BAD_REQUEST)


class TestCeleryView(APIView):
    def get(self, request):
        # 用celery异步执行debug
        debug_task.delay()
        return Response({'detail':'成功!'})