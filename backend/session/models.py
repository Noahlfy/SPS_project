from django.db import models

class Session(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        PAUSED = 'paused', 'Paused'
        COMPLETED = 'completed', 'Completed'

    session_id = models.AutoField(primary_key=True)  # Use AutoField for automatic primary key
    session_name = models.CharField(max_length=50, default="Default Session")
    start_time = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    end_time = models.DateTimeField(auto_now_add=True)  # Allow null values
    acceleration_max = models.FloatField(null=True, blank=True)
    speed_max = models.FloatField(null=True, blank=True)
    total_distance = models.FloatField(null=True, blank=True)
    concussion_risk = models.IntegerField(null=True, blank=True)
    fatigue_level = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return self.session_name

    class Meta:
        db_table = "training_sessions"
