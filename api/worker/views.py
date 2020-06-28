from django.shortcuts import render
from rest_framework import viewsets
from worker.serializers import WorkerSerializer
from worker.models import Worker

# ViewSets define the view behavior.
class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
