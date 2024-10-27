from django.db import models

from session.models import Session

class HeartRate(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField()
    SpO2 = models.FloatField()
    BPM = models.IntegerField()

    class Meta:
        db_table = 'MAX30102'
        ordering = ['time']