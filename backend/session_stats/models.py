from django.db import models
from session.models import Session


class SessionStats(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField()
    distance = models.FloatField()
    pace = models.FloatField()
    g = models.FloatField()
    BPM = models.FloatField()
    footing_quality = models.FloatField()
    fatigue_level = models.FloatField(null=True, blank=True)
    training_intensity = models.FloatField()
    concussion_risk = models.FloatField()
    
    class Meta:
        db_table = 'session_stats'
        ordering = ['time']