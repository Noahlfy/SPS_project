from django.db import models
from session.models import Session

class DashboardStats(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField()
    training_productivity = models.FloatField()
    concussion_risk = models.FloatField()
    rest_days = models.FloatField()
    concussion_passeport = models.FloatField()
    training_intensity = models.FloatField()
    heart_rate = models.FloatField()
    
    class Meta:
        db_table = 'dashboard_stats'
        ordering = ['time']