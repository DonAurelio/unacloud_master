from django.db import models

from worker.models import WorkerNode

# Create your models here.


class ExecutionEnvironment(models.Model):

    PENDING = '0'
    SCHEDULED = '1'
    RUNNING = '2'
    SUCCESS = '3'
    FAILED = '4'
    UNKNOWN = '5'

    STATUS_CHOICES = (
        (PENDING,'Pending'),
        (SCHEDULED,'Scheduled'),
        (RUNNING, 'Running'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (UNKNOWN, 'Unknown')
    )

    VIRTUALBOX = '0'

    PROVIDER_CHOICES = (
        (VIRTUALBOX,'virtualbox'),
    )

    provider = models.CharField(max_length=2,choices=PROVIDER_CHOICES)
    cpus = models.IntegerField()
    memory = models.IntegerField()
    status = models.CharField(max_length=2,choices=STATUS_CHOICES)
    worker = models.ForeignKey(WorkerNode,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)