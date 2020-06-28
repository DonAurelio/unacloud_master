from django.db import models


class WorkerNode(models.Model):

    address = models.GenericIPAddressField(protocol='IPv4')
    cpus = models.IntegerField()
    cpus_reserved = models.IntegerField(default=0)
    memory = models.IntegerField()
    memory_reserved = models.IntegerField(default=0)
    last_health_report_date = models.DateTimeField(null=True)
