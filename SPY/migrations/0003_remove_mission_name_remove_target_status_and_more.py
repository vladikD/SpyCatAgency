# Generated by Django 5.1.3 on 2024-11-09 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SPY', '0002_remove_mission_is_complete_remove_target_is_complete_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mission',
            name='name',
        ),
        migrations.RemoveField(
            model_name='target',
            name='status',
        ),
        migrations.AddField(
            model_name='target',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='spycat',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='target',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='target',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
