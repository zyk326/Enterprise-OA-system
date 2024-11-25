from http.client import responses

from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.views import APIView

from .models import Absent, AbsentType, AbsentStatusChoices
from .serializers import AbsentSerializer, AbsentTypeSerializer
from rest_framework.response import Response

from .utils import get_responder
from apps.oaauth.serializers import UserSerializer


# Create your views here.
# 1.发起考勤 creat
# 2.处理考勤 update
# 3.查看自己的考勤列表 list?who=my
# 4.查看下属的考勤列表 list?who=sub
class AbsentViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Absent.objects.all()
    serializer_class = AbsentSerializer

    def update(self, request, *args, **kwargs):
        # 默认情况下,如果要修改某一条数据,要传入这个数据序列化中的所有字段
        # 如果只想修改一部分数据,那么可以在kwargs中设置partial为True
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        who = request.query_params.get('who')
        if who and who == 'sub':
            result = queryset.filter(responder=request.user)
        else:
            result = queryset.filter(requester=request.user)

        page = self.paginate_queryset(result)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)    # 这里会做分页逻辑

        serialize = self.serializer_class(result, many=True)
        return Response(data=serialize.data)

class AbsentTypeView(APIView):
    def get(self, request):
        types = AbsentType.objects.all()
        serializer = AbsentTypeSerializer(types, many=True)
        return Response(serializer.data)

class ResponderView(APIView):
    def get(self, request):
        responder = get_responder(request)
        serializer = UserSerializer(responder)
        return Response(data=serializer.data)