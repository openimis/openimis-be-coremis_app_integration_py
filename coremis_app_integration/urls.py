from django.urls import path
from coremis_app_integration.endpoints import login

urlpatterns = [
    path('api/mobile/v1/user/login', login),
]
