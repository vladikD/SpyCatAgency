# Generated by Django 5.1.3 on 2024-11-09 18:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SPY', '0005_mission_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='cat',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mission', to='SPY.spycat'),
        ),
    ]
