# Generated by Django 5.1.2 on 2024-11-01 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0002_alter_session_concussion_risk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='acceleration_max',
        ),
        migrations.RemoveField(
            model_name='session',
            name='concussion_risk',
        ),
        migrations.RemoveField(
            model_name='session',
            name='fatigue_level',
        ),
        migrations.RemoveField(
            model_name='session',
            name='speed_max',
        ),
        migrations.RemoveField(
            model_name='session',
            name='total_distance',
        ),
    ]
