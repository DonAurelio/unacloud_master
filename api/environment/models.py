from django.db import models

from worker.models import Worker


class Environment(models.Model):

    # Environtment status
    OFF = 'Off'
    RUNNING = 'Running'
    REBOOTING = 'Rebooting'
    DELETED = 'Deleted'
    NO_DEPLOYED = 'No Deployed'
    UNKNOWN = 'Unknown'

    STATUS_CHOICES = (
        (OFF,'Off'),
        (RUNNING,'Running'),
        (REBOOTING, 'Rebooting'),
        (DELETED, 'Deleted'),
        (NO_DEPLOYED,'No Deployed'),
        (UNKNOWN, 'Unknown'),
    )

    # Environment provider
    VIRTUALBOX = 'virtualbox'

    PROVIDER_CHOICES = (
        (VIRTUALBOX,'virtualbox'),
    )

    # Environment name, it must be unike for every user.
    name = models.CharField(max_length=50,unique=True)
    # Hypervisor
    provider = models.CharField(max_length=50,choices=PROVIDER_CHOICES)
    # IPAddress assin
    address = models.GenericIPAddressField(protocol='IPv4',unique=True,null=True,blank=True)
    # Connection port
    ssh_port = models.PositiveSmallIntegerField(null=True,blank=True)
    # Number of cores for the environment
    cores = models.PositiveSmallIntegerField()
    # Memory in MB
    memory = models.PositiveSmallIntegerField()
    # Environment status
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,null=True,blank=True)
    # Environmet last status report
    last_report_date = models.DateTimeField(null=True,blank=True)
    # Worker running the environment
    worker = models.ForeignKey(Worker,on_delete=models.CASCADE,null=True,blank=True)


class Deployment(models.Model):

    PENDING = 'Pending'
    SCHEDULED = 'Scheduled'
    DISPATCHED = 'Dispatched'
    RUNNING = 'Running'
    SUCCESS = 'Success'
    FAILED = 'Failed'
    UNKNOWN = 'Unknown'

    STATUS_CHOICES = (
        (PENDING,'Pending'),
        (SCHEDULED,'Scheduled'),
        (DISPATCHED,'Dispatched'),
        (RUNNING, 'Running'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (UNKNOWN, 'Unknown')
    )

    environment = models.OneToOneField(Environment,on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=PENDING)
    detail = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)


