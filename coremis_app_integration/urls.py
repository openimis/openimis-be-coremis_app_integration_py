from django.urls import path
from coremis_app_integration.endpoints import (
    login,
    change_password
)

urlpatterns = [
    path('api/mobile/v1/user/login', login),
    path('api/mobile/v1/user/password/change', change_password),
]
