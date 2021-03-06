# Generated by Django 3.0.7 on 2020-06-29 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('environment', '0003_auto_20200628_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='environment',
            name='ssh_port',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Scheduled', 'Scheduled'), ('Dispatched', 'Dispatched'), ('Running', 'Running'), ('Success', 'Success'), ('Failed', 'Failed'), ('Unknown', 'Unknown')], default='Pending', max_length=50),
        ),
    ]
