from rest_framework import serializers

from environment.models import Environment
from environment.models import Deployment
from environment.models import Action

class EnvironmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Environment
        fields = [
            'id','url','name','provider','address','deployment',
            'cores','memory','status','last_report_date','worker'
        ]


class DeploymentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Deployment
        fields = [
            'id','url','environment','status','detail',
            'created_at'
        ]


class ActionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Action
        fields = [
            'id','url','action','environment','status','detail',
            'created_at'
        ]