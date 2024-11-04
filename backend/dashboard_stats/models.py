from django.db import models
from session.models import Session

class DashboardStats(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField()
    training_productivity = models.FloatField(null=True, blank=True)
    concussion_risk = models.FloatField(null=True, blank=True)
    rest_days = models.FloatField(null=True, blank=True)
    concussion_passeport = models.FloatField(null=True, blank=True)
    training_intensity = models.FloatField(null=True, blank=True)
    heart_rate = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'dashboard_stats'
        ordering = ['time']