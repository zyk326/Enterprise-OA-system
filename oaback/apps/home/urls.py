from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('latest/inform', views.LatestInformView.as_view(), name='LatestInform'),
    path('latest/absent', views.LatestAbsentView.as_view(), name='LatestAbsent'),
    path('department/staff/count', views.DepartmentStaffView.as_view(), name='DepartmentStaff'),

]