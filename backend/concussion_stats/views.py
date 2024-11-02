from rest_framework import viewsets

from concussion_stats.models import ConcussionStats

from concussion_stats.serializers import ConcussionStatsSerializer

class ConcussionStatsViewSet(viewsets.ModelViewSet):
    queryset = ConcussionStats.objects.all()
    serializer_class = ConcussionStatsSerializer