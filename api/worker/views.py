from django.shortcuts import render
from rest_framework import viewsets
from worker.serializers import WorkerNodeSerializer
from worker.models import WorkerNode

# ViewSets define the view behavior.
class WorkerNodeViewSet(viewsets.ModelViewSet):
    queryset = WorkerNode.objects.all()
    serializer_class = WorkerNodeSerializer
    # permission_classes = []

