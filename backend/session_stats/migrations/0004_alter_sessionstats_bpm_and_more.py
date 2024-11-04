# Generated by Django 5.1.2 on 2024-11-02 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session_stats', '0003_alter_sessionstats_fatigue_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionstats',
            name='BPM',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sessionstats',
            name='concussion_risk',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sessionstats',
            name='footing_quality',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sessionstats',
            name='training_intensity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
