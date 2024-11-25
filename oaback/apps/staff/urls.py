from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('departments', views.DepartmentListView.as_view(), name='departments'),
]