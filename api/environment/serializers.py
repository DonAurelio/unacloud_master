from rest_framework import serializers

from environment.models import Environment
from environment.models import Deployment
from environment.models import Action

class EnvironmentSerializer(serializers.HyperlinkedModelSerializer):

    worker_id = serializers.SerializerMethodField()

    class Meta:
        model = Environment
        fields = [
            'id','url','name','ssh_port','worker_id','provider','address','deployment',
            'cores','memory','status','last_report_date','worker'
        ]


    def get_worker_id(self,obj):
        if obj.worker:
            return obj.worker.id
        else:
            return None

class DeploymentSerializer(serializers.HyperlinkedModelSerializer):

    environment_name = serializers.SerializerMethodField()

    class Meta:
        model = Deployment
        fields = [
            'id','url','environment','environment_name','status','detail',
            'created_at'
        ]

    def get_environment_name(self,obj):
        return obj.environment.name

class ActionSerializer(serializers.HyperlinkedModelSerializer):

    environment_name = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = [
            'id','url','action','environment_name','environment','status','detail',
            'created_at'
        ]

    def get_environment_name(self,obj):
        return obj.environment.name