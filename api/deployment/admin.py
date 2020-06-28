from django.contrib import admin
from deployment.models import ExecutionEnvironment


class ExecutionEnvironmentAdmin(admin.ModelAdmin):
    fields = (
        'provider','cpus','memory',
        'status', 'worker'
    )

    list_display = (
        'provider','cpus','memory',
        'status', 'worker', 'created_at'
    )

admin.site.register(ExecutionEnvironment, ExecutionEnvironmentAdmin)