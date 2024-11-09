# Generated by Django 5.1.3 on 2024-11-09 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SPY', '0003_remove_mission_name_remove_target_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='target',
            name='mission',
        ),
        migrations.AlterField(
            model_name='spycat',
            name='breed',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='spycat',
            name='years_of_experience',
            field=models.PositiveIntegerField(),
        ),
        migrations.DeleteModel(
            name='Mission',
        ),
        migrations.DeleteModel(
            name='Target',
        ),
    ]
