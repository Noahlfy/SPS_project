from django.db import models
from session.models import Session

# def insert_concussion_stats(self, session_id, time, footing_quality, number_of_shocks, max_g, heart_rate, SpO2, temperature) :
#         self.cursor.execute('''
#         INSERT INTO concussion_stats (session_id, time, footing_quality, number_of_shocks, max_g, heart_rate, SpO2, temperature)
#         VALUES (?, ?, ?, ?, ?, ?)
#         ''', (session_id, time, footing_quality, number_of_shocks, max_g, heart_rate, SpO2, temperature))
#         self.connection.commit()

class ConcussionStats(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField()
    footing_quality = models.FloatField()
    number_of_shocks = models.IntegerField()
    max_g = models.FloatField()
    BMP = models.FloatField()
    SpO2 = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        db_table = 'concussion_stats'
        ordering = ['time']