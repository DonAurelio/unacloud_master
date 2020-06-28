from django.contrib import admin
from worker.models import Worker

# Register your models here.
class WorkerAdmin(admin.ModelAdmin):
    fields = (
        'address','cpus','cpus_reserved',
        'memory','memory_reserved',
    )

    list_display = (
        'id','address','cpus','cpus_reserved',
        'memory','memory_reserved',
		'last_health_report_date'
    )

admin.site.register(Worker, WorkerAdmin)