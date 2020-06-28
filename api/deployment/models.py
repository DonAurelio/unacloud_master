from django.db import models

from worker.models import WorkerNode

# Create your models here.


class ExecutionEnvironment(models.Model):

    PENDING = 'Pending'
    SCHEDULED = 'Scheduled'
    RUNNING = 'Running'
    SUCCESS = 'Success'
    FAILED = 'Failed'
    UNKNOWN = 'Unknown'

    STATUS_CHOICES = (
        (PENDING,'Pending'),
        (SCHEDULED,'Scheduled'),
        (RUNNING, 'Running'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (UNKNOWN, 'Unknown')
    )

    VIRTUALBOX = 'virtualbox'

    PROVIDER_CHOICES = (
        (VIRTUALBOX,'virtualbox'),
    )

    provider = models.CharField(max_length=50,choices=PROVIDER_CHOICES)
    cpus = models.PositiveSmallIntegerField()
    memory = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=PENDING)
    detail = models.TextField(null=True,blank=True)
    worker = models.ForeignKey(WorkerNode,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)