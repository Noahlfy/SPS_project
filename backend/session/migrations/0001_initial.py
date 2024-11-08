# Generated by Django 5.1.2 on 2024-10-27 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Session",
            fields=[
                ("session_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "session_name",
                    models.CharField(default="Default Session", max_length=50),
                ),
                ("start_time", models.DateTimeField(auto_now_add=True)),
                ("end_time", models.DateTimeField(auto_now_add=True)),
                ("acceleration_max", models.FloatField(blank=True, null=True)),
                ("speed_max", models.FloatField(blank=True, null=True)),
                ("total_distance", models.FloatField(blank=True, null=True)),
                ("concussion_risk", models.IntegerField(blank=True, null=True)),
                ("fatigue_level", models.FloatField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("paused", "Paused"),
                            ("completed", "Completed"),
                        ],
                        default="active",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "db_table": "training_sessions",
            },
        ),
    ]
