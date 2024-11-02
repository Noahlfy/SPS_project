from rest_framework import viewsets

from .models import Head

from .serializers import HeadSerializer

class HeadViewSet(viewsets.ModelViewSet):
    queryset = Head.objects.all()
    serializer_class = HeadSerializer
