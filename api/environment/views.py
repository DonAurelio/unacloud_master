from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import views
from rest_framework import status

from environment.serializers import EnvironmentSerializer
from environment.serializers import DeploymentSerializer
from environment.serializers import ActionSerializer
from environment.models import Deployment
from environment.models import Environment
from environment.models import Action

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


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
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

class ActionDeploymentStatusUpdate(views.APIView):

    def post(self,request,format=None):
        data = request.data
        is_success = data.get('action_is_success')
        if is_success:
            action_id = data.get('action_id')
            action_obj = Action.objects.get(id=action_id)
            print(action_obj.action)
            if action_obj.action in Action.START:
                action_obj.environment.status = Environment.RUNNING
            elif action_obj.action in Action.STOP:
                action_obj.environment.status = Environment.OFF
            elif action_obj.action in Action.RESET:
                action_obj.environment.status = Environment.RUNNING
            elif action_obj.action in Action.DELETE:
                action_obj.environment.status = Environment.DELETED
            else:
                action_obj.environment.status = Environment.UNKNOWN

            action_obj.environment.save()
            action_obj.status = Action.SUCCESS
            action_obj.save()

        else:
            action_id = data.get('action_id')
            message = data.get('message')
            action_obj = Action.objects.get(id=action_id)
            action_obj.status = Action.FAILED
            action_obj.detail = message
            action_obj.save()

        return Response({'message':'Done'})

class EnvironmentCreate(views.APIView):

    def post(self,request,format=None):
        data = request.data

        try:
            environment = Environment(
                name=data.get('name'),
                provider=data.get('provider'),
                cores=data.get('cpus'),
                memory=data.get('memory')
            )

            environment.save()
        except IntegrityError as e:
            message = "An environment with name '%s' already exists !!" % data.get('name')
            return Response({'message':message},status=status.HTTP_200_OK)

        message = "environment '%s' created !!" % data.get('name')
        return Response({'message': message},status=status.HTTP_201_CREATED)

class EnvironmentAction(views.APIView):

    def post(self,request,format=None):
        data = request.data

        environment_name = data.get('environment_name')
        action_type = data.get('action')

        try:
            environment = Environment.objects.get(name=environment_name)
            if not environment.status:
                message = "environment '%s' is not deployed yet !!" % environment_name
                return Response({'message':message},status=status.HTTP_200_OK)

            action = Action(
                environment=environment,
                action=data.get('action'),
            )

            action.save()

        except Environment.DoesNotExist as e:
            message = "environment '%s' does not exists !!" % environment_name
            return Response({'message':message},status=status.HTTP_200_OK)


        message = "action '%s' created !!" % action_type
        return Response({'message':message},status=status.HTTP_201_CREATED)