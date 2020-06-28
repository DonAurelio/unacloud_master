from django.contrib import admin
from worker.models import WorkerNode

# Register your models here.
class WorkerNodeAdmin(admin.ModelAdmin):
    fields = (
        'address','cpus','cpus_reserved',
        'memory','memory_reserved',
    )

    list_display = (
        'id','address','cpus','cpus_reserved',
        'memory','memory_reserved',
		'last_health_report_date'
    )

admin.site.register(WorkerNode, WorkerNodeAdmin)