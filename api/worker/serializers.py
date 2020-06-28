from rest_framework import serializers
from worker.models import WorkerNode

class WorkerNodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkerNode
        fields = [
        	'id','address','cpus', 'memory', 'last_health_report_date'
        ]