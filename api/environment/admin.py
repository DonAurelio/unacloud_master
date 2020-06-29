from django.contrib import admin
from environment.models import Environment
from environment.models import Deployment
from environment.models import Action


class EnvironmentAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'provider','address',
        'cores','memory','status',
        'last_report_date','worker'
    )

    list_display = (
        'id','provider','address','ssh_port',
        'cores','memory','status',
        'last_report_date','worker'
    )

admin.site.register(Environment, EnvironmentAdmin)


class DeploymentAdmin(admin.ModelAdmin):
    fields = (
       'environment','status','detail'
    )

    list_display = (
        'id','environment','status',
        'detail','created_at'
    )

admin.site.register(Deployment, DeploymentAdmin)


class ActionAdmin(admin.ModelAdmin):
    fields = (
       'action','environment','status','detail'
    )

    list_display = (
        'id','action','environment','status',
        'detail','created_at'
    )

admin.site.register(Action, ActionAdmin)