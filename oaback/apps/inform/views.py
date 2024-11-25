from rest_framework import viewsets
from apps.inform.models import Inform
from apps.inform.serializers import InformSerializer


class InformViewSet(viewsets.ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer