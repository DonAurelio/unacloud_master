# Generated by Django 3.0.7 on 2020-06-28 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0005_auto_20200628_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workernode',
            name='cpus_reserved',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='workernode',
            name='memory_reserved',
            field=models.IntegerField(default=0),
        ),
    ]