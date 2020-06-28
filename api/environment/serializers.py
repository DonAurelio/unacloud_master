from rest_framework import serializers

from environment.models import Environment


class EnvironmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Environment
        fields = [
            'id','name','provider','address',
            'cores','memory','status','last_report_date',
            'deployment','worker'
        ]


class EnvironmentDeploymentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Environment
        fields = [
            'id','environment','status','detail',
            'created_at'
        ]

