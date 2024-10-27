from rest_framework import viewsets

from .models import HeartRate

from .serializers import HeartRateSerializer

class HeartRateViewSet(viewsets.ModelViewSet):
    queryset = HeartRate.objects.all()
    serializer_class = HeartRateSerializer