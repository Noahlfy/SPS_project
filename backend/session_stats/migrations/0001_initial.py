# Generated by Django 5.1.2 on 2024-11-01 22:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('session', '0003_remove_session_acceleration_max_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('distance', models.FloatField()),
                ('pace', models.FloatField()),
                ('g', models.FloatField()),
                ('heart_rate', models.FloatField()),
                ('footing_quality', models.FloatField()),
                ('fatigue_level', models.FloatField()),
                ('training_intensity', models.FloatField()),
                ('concussion_risk', models.FloatField()),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.session')),
            ],
            options={
                'db_table': 'session_stats',
                'ordering': ['time'],
            },
        ),
    ]