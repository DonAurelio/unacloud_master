from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from environment.serializers import EnvironmentSerializer
from environment.serializers import DeploymentSerializer
from environment.models import Deployment
from environment.models import Environment

import django_filters.rest_framework


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['status','deployment__status','worker']


    def partial_update(self, request, pk=None):
        """Handless updating prt of an object."""

        return Response({'http_method':'PATH'})

class DeploymentViewSet(viewsets.ModelViewSet):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['status']


    def partial_update(self, request, pk=None):
        """Handless updating prt of an object."""

        return Response({'http_method':'PATH'})