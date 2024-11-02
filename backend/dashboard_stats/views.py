from rest_framework import viewsets

from dashboard_stats.models import DashboardStats

from dashboard_stats.serializers import DashboardStatsSerializer

class DashboardStatsViewSet(viewsets.ModelViewSet):
    queryset = DashboardStats.objects.all()
    serializer_class = DashboardStatsSerializer