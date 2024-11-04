from django.db import models
from session.models import Session

class ChestMemory(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField()
    g_measurement = models.FloatField()
    velocity_norm = models.FloatField()
    distance = models.FloatField()

    class Meta:
        db_table = 'BNO055_chest_memory'
        ordering = ['time']