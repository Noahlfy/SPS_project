from rest_framework import viewsets

from .models import Chest

from .serializers import ChestSerializer

class ChestViewSet(viewsets.ModelViewSet):
    queryset = Chest.objects.all()
    serializer_class = ChestSerializer