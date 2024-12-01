from rest_framework.response import Response
from rest_framework.views import APIView
from apps.inform.models import Inform, InformRead
from apps.inform.serializers import InformSerializer
from django.db.models import Q, Prefetch
from apps.absent.serializers import AbsentSerializer
from apps.absent.models import Absent
from apps.oaauth.models import OADepartment
from django.db.models import Count
# 函数的
from django.views.decorators.cache import cache_page
# 类的某个方法
from django.utils.decorators import method_decorator

# @cache_page(60 * 15)
# def cache_demo_view(request):
#     pass

class LatestInformView(APIView):
    '''
    返回最新的十条通知
    '''
    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        current_user = request.user
        # 返回公共或者所在部门能看到的通知
        informs = Inform.objects.prefetch_related(Prefetch("reads", queryset=InformRead.objects.filter(user_id=current_user.uid)), 'departments').filter(Q(public=True) | Q(departments=current_user.department))[:10]
        serializer = InformSerializer(informs, many=True)
        return Response(serializer.data)

class LatestAbsentView(APIView):
    '''
    董事会的人,可以看到所有人的考勤信息,非董事会的人只能看到自己部门的考勤信息
    '''
    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        current_user = request.user
        queryset = Absent.objects
        if current_user.department.name != '董事会':
            queryset = queryset.filter(requester__department_id=current_user.department_id)
        queryset = queryset.all()[:10]
        serializer = AbsentSerializer(queryset, many=True)
        return Response(serializer.data)

class DepartmentStaffView(APIView):
    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        rows = OADepartment.objects.annotate(staff_count=Count('staffs')).values("name", "staff_count")
        print('='*10)
        return Response(rows)