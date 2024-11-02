from django.db import models
from session.models import Session
# Create your models here.

class LeftLegTransformed(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    accel_x = models.FloatField()
    accel_y = models.FloatField()
    accel_z = models.FloatField()
    vel_x = models.FloatField()
    vel_y = models.FloatField()
    vel_z = models.FloatField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    
    class Meta:
        db_table = 'BNO055_left_leg_transformed'
        ordering = ['timestamp']