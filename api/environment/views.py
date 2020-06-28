from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from environment.serializers import EnvironmentSerializer
from environment.serializers import EnvironmentDeploymentSerializer
from environment.models import EnvironmentDeployment
from environment.models import Environment

import django_filters.rest_framework


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['status']


    def partial_update(self, request, pk=None):
        """Handless updating prt of an object."""

        return Response({'http_method':'PATH'})

class EnvironmentDeploymentViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentDeployment.objects.all()
    serializer_class = EnvironmentDeploymentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['status']


    def partial_update(self, request, pk=None):
        """Handless updating prt of an object."""

        return Response({'http_method':'PATH'})