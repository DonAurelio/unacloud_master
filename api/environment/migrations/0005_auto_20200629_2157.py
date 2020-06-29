# Generated by Django 3.0.7 on 2020-06-29 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('environment', '0004_auto_20200629_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='last_report_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='environment',
            name='status',
            field=models.CharField(blank=True, choices=[('Off', 'Off'), ('Running', 'Running'), ('Rebooting', 'Rebooting'), ('Deleted', 'Deleted'), ('No Deployed', 'No Deployed'), ('Unknown', 'Unknown')], max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('Pending', 'Pending'), ('Scheduled', 'Scheduled'), ('Dispatched', 'Dispatched'), ('Running', 'Running'), ('Success', 'Success'), ('Failed', 'Failed'), ('Unknown', 'Unknown')], max_length=50)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Scheduled', 'Scheduled'), ('Dispatched', 'Dispatched'), ('Running', 'Running'), ('Success', 'Success'), ('Failed', 'Failed'), ('Unknown', 'Unknown')], default='Pending', max_length=50)),
                ('detail', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('environment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='environment.Environment')),
            ],
        ),
    ]
