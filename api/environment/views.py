from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import views

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


class DeploymentViewSet(viewsets.ModelViewSet):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['status']


class EnviromentDeploymentStatusUpdate(views.APIView):

    def post(self,request,format=None):

        data = request.data
        is_success = data.get('deployment_is_success')
        if is_success:
            # statistics is not used, but soon will 
            # contain deployment statistics
            statistics = data.get('statistics')

            environment = data.get('environment')
            environment_id = environment.get('id')
            environment_obj = Environment.objects.get(id=environment_id)
            environment_obj.address = environment.get('address')
            environment_obj.ssh_port = environment.get('ssh_port')
            environment_obj.status = Environment.RUNNING
            environment_obj.deployment.status = Deployment.SUCCESS
            environment_obj.deployment.save()

            environment_obj.save()

        else:
            message = data.get('message')
            environment = data.get('environment')
            environment_id = environment.get('id')
            environment_obj = Environment.objects.get(id=environment_id)
            environment_obj.status = Environment.NO_DEPLOYED
            environment_obj.deployment.status = Deployment.FAILED
            environment_obj.deployment.detail = message
            environment_obj.deployment.save()
            environment_obj.save()

        return Response({'message':'Done'})