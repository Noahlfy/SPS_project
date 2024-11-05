from django.db import models
from session.models import Session


class ConcussionStats(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField()
    footing_quality = models.FloatField(null=True, blank=True)
    number_of_shocks = models.IntegerField(null=True, blank=True)
    max_g = models.FloatField(null=True, blank=True)
    BMP = models.FloatField(null=True, blank=True)
    SpO2 = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'concussion_stats'
        ordering = ['time']