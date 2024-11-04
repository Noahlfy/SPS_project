from django.db import models
from session.models import Session


class SessionStats(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField()
    distance = models.FloatField(null=True, blank=True)
    pace = models.FloatField(null=True, blank=True)
    g = models.FloatField(null=True, blank=True)
    BPM = models.FloatField(null=True, blank=True)
    footing_quality = models.FloatField(null=True, blank=True)
    fatigue_level = models.FloatField(null=True, blank=True)
    training_intensity = models.FloatField(null=True, blank=True)
    concussion_risk = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'session_stats'
        ordering = ['time']