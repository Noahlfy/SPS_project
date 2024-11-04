# Generated by Django 5.1.2 on 2024-11-04 11:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('session', '0003_remove_session_acceleration_max_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeftLegMemory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('g_measurement', models.FloatField()),
                ('velocity_norm', models.FloatField()),
                ('distance', models.FloatField()),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.session')),
            ],
            options={
                'db_table': 'BNO055_left_leg_memory',
                'ordering': ['time'],
            },
        ),
    ]
