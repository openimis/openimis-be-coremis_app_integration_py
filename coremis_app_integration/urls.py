from django.urls import path
from coremis_app_integration.endpoints import (
    login,
    change_password,
    payment_details
)

urlpatterns = [
    path('api/mobile/v1/user/login', login),
    path('api/mobile/v1/user/password/change', change_password),
    path('api/mobile/v1/payment/details/channel', payment_details),
]
