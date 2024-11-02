# Generated by Django 5.1.2 on 2024-11-01 20:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head_transformed', '0001_initial'),
        ('session', '0002_alter_session_concussion_risk'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='headtransformed',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterField(
            model_name='headtransformed',
            name='session_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.session'),
        ),
        migrations.AlterModelTable(
            name='headtransformed',
            table='BNO055_head_transformed',
        ),
    ]