# Generated by Django 5.1.2 on 2024-11-02 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session_stats', '0002_rename_heart_rate_sessionstats_bpm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionstats',
            name='fatigue_level',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
