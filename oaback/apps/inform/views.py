from venv import create

from rest_framework import viewsets
from rest_framework.views import APIView

from apps.inform.models import Inform, InformRead
from apps.inform.serializers import InformSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import InformReadSerializer
from django.db.models import Prefetch


class InformViewSet(viewsets.ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer

    # 通知列表
    def get_queryset(self):
        # 多个条件的并差用Q函数
        # prefetch_related('reads') 把read表中存在的多对多的关系存在的条目查出来
        return self.queryset.select_related('author').prefetch_related(Prefetch("reads", queryset=InformRead.objects.filter(user_id=self.request.user.uid)), 'departments').filter(Q(public=True) | Q(departments=self.request.user.department) | Q(author=self.request.user)).distinct()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.uid == request.user.uid:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class InformReadView(APIView):
    def post(self, request):
        serializer = InformReadSerializer(data=request.data)
        if serializer.is_valid():
            inform_pk = serializer.validated_data.get('inform_pk')
            if InformRead.objects.filter(inform_id=inform_pk, user_id=request.user.uid).exists():
                return Response()
            else:
                try:
                    InformRead.objects.create(inform_id=inform_pk, user_id=request.user.uid)
                    return Response()
                except Exception as e:
                    print(e)
                    return Response(data={'detail':'阅读失败！'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'detail':list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)