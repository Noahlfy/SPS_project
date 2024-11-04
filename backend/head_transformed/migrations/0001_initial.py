# Generated by Django 5.1.2 on 2024-11-01 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeadTransformed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('accel_x', models.FloatField()),
                ('accel_y', models.FloatField()),
                ('accel_z', models.FloatField()),
                ('vel_x', models.FloatField()),
                ('vel_y', models.FloatField()),
                ('vel_z', models.FloatField()),
                ('pos_x', models.FloatField()),
                ('pos_y', models.FloatField()),
                ('pos_z', models.FloatField()),
            ],
        ),
    ]