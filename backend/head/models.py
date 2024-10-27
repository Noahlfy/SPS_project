from django.db import models
from session.models import Session

# Create your models here.

class Head(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)  # ForeignKey to Session
    time = models.DateTimeField()
    accel_x = models.FloatField()
    accel_y = models.FloatField()
    accel_z = models.FloatField()
    quat_w = models.FloatField()
    quat_x = models.FloatField()
    quat_y = models.FloatField()
    quat_z = models.FloatField()

    class Meta:
        db_table = 'BNO055_head'
        ordering = ['time']