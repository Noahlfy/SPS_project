from django.db import models

from session.models import Session

class Temperature(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField()
    temperature = models.FloatField()
    pressure = models.FloatField()

    class Meta:
        db_table = 'BMP280'
        ordering = ['time']