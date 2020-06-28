from rest_framework import serializers
from worker.models import Worker

class WorkerSerializer(serializers.HyperlinkedModelSerializer):

    # assosiated with get_available_cores
    available_cpus = serializers.SerializerMethodField()
    # associated with get_available memory
    get_available_memory = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = [
            'id','url','address',
            'cpus', 'cpus_reserved','available_cpus',
            'memory', 'memory_reserved','available_memory',
            'last_health_report_date'
        ]


    def get_available_cpus(self,obj):
        return obj.available_cpus

    def get_available_memory(self,obj):
        return obj.available_memory
