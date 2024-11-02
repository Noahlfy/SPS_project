from rest_framework import serializers

from session_stats.models import SessionStats

class SessionStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionStats
        fields = '__all__'