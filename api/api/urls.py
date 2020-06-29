"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework import routers
from worker.views import WorkerViewSet
from environment.views import EnvironmentViewSet
from environment.views import DeploymentViewSet
from environment.views import EnviromentDeploymentStatusUpdate


# Register here only viewsets, APIView and other go down in urlpatterns
router = routers.DefaultRouter()
router.register(r'worker/workers', WorkerViewSet)
router.register(r'environment/environments', EnvironmentViewSet)
router.register(r'environment/deployments', DeploymentViewSet)


urlpatterns = [
    path('', admin.site.urls),
	path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/environment/deployment/status_update/',EnviromentDeploymentStatusUpdate.as_view())
]
