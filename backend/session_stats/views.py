from rest_framework import viewsets

from session_stats.models import SessionStats

from session_stats.serializers import SessionStatsSerializer

class SessionStatsViewSet(viewsets.ModelViewSet):
    queryset = SessionStats.objects.all()
    serializer_class = SessionStatsSerializer