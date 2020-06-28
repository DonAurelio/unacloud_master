from django.contrib import admin
from environment.models import Environment
from environment.models import Deployment


class EnvironmentAdmin(admin.ModelAdmin):
    fields = (
        'provider','address',
        'cores','memory','status',
        'last_report_date','worker'
    )

    list_display = (
        'id','provider','address',
        'cores','memory','status',
        'last_report_date','worker'
    )

admin.site.register(Environment, EnvironmentAdmin)


class DeploymentAdmin(admin.ModelAdmin):
    fields = (
        'environment','status',
        'detail','created_at'
    )

    list_display = (
        'id','environment','status',
        'detail','created_at'
    )

admin.site.register(Deployment, DeploymentAdmin)