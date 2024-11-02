from rest_framework import serializers

from dashboard_stats.models import DashboardStats

class DashboardStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardStats
        fields = '__all__'