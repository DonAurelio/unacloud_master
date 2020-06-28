# Generated by Django 3.0.7 on 2020-06-28 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='executionenvironment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='executionenvironment',
            name='provider',
            field=models.CharField(choices=[('0', 'virtualbox')], max_length=2),
        ),
        migrations.AlterField(
            model_name='executionenvironment',
            name='status',
            field=models.CharField(choices=[('0', 'Pending'), ('1', 'Scheduled'), ('2', 'Running'), ('3', 'Success'), ('4', 'Failed'), ('5', 'Unknown')], max_length=2),
        ),
    ]