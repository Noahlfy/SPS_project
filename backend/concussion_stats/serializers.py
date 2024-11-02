from rest_framework import serializers

from concussion_stats.models import ConcussionStats

class ConcussionStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcussionStats
        fields = '__all__'