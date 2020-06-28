from rest_framework import serializers
from deployment.models import ExecutionEnvironment

class ExecutionEnvironmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExecutionEnvironment
        fields = [
            'id','provider','cpus', 'memory', 
            'status','detail','worker', 'created_at'
        ]

