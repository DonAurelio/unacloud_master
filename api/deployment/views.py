from django.shortcuts import render
from rest_framework import viewsets
from deployment.serializers import ExecutionEnvironmentSerializer
from deployment.models import ExecutionEnvironment
from rest_framework.response import Response

import django_filters.rest_framework


# ViewSets define the view behavior.
class ExecutionEnvironmentViewSet(viewsets.ModelViewSet):
    queryset = ExecutionEnvironment.objects.all()
    serializer_class = ExecutionEnvironmentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['status']



    def partial_update(self, request, pk=None):
    	"""Handless updating prt of an object."""

    	return Response({'http_method':'PATH'})
