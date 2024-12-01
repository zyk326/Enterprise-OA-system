from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'staff'

# 去掉尾巴的/ trailing
router = DefaultRouter(trailing_slash=False)
router.register('staff', views.StaffViewSet, basename='staff_view')

urlpatterns = [
    path('departments', views.DepartmentListView.as_view(), name='departments'),
    # path("staff", views.StaffView.as_view(), name='staff_view'),
    path('active', views.ActiveStaffView.as_view(), name='active_view'),
    path('test/celery', views.TestCeleryView.as_view(), name='test_celery'),
    path('download', views.StaffDownloadView.as_view(), name='staff_download'),
    path('upload', views.StaffUploadView.as_view(), name='staff_upload'),
] + router.urls