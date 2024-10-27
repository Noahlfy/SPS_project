from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Session

from .serializers import SessionSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
