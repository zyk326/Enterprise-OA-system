from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path
from . import views

app_name = 'inform'

router = DefaultRouter(trailing_slash=False)
router.register('inform', views.InformViewSet, basename='inform')

urlpatterns = [
    path('inform/read', views.InformReadView.as_view(), name='inform_read'),
] + router.urls