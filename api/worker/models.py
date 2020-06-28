from django.db import models


class Worker(models.Model):

    address = models.GenericIPAddressField(protocol='IPv4',unique=True)
    cpus = models.PositiveSmallIntegerField()
    cpus_reserved = models.PositiveSmallIntegerField(default=0)
    memory = models.PositiveSmallIntegerField()
    memory_reserved = models.PositiveSmallIntegerField(default=0)
    last_health_report_date = models.DateTimeField(null=True)

    @property
    def available_cpus(self):
    	return self.cpus - self.cpus_reserved

    @property
    def available_memory(self):
    	return self.memory - self.memory_reserved
