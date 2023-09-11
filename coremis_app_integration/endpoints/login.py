from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import authenticate
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
    api_view
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from coremis_app_integration.authorization import (
    CustomBasicAuthentication,
    DETAILS,
    FAILED,
    SUCCESS
)
from payroll.models import PaymentPoint


@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
@permission_classes([IsAuthenticated])
def login(request):
    # check if user is assigned to any PaymentPoint entity which indicates ppm user role
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    authenticated_user = authenticate(username=username, password=password)
    if authenticated_user:
        payment_points = PaymentPoint.objects.filter(ppm__username=username)
        if payment_points.count() > 0:
            response_data = SUCCESS
            response_data["result"] = _build_success_output(authenticated_user)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response = FAILED
            response['result'] = _('Payment Point Manager not assigned to any PaymentPoints')
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
    else:
        response = FAILED
        response['result'] = _(
            'Wrong request authentication data. '
            'Please correct username or password'
        )
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)


def _build_success_output(user):
    response_success_details = DETAILS
    response_success_details['id'] = user.id
    response_success_details['username'] = user.username
    response_success_details['fullname'] = user.username
    response_success_details['lastLogin'] = user.last_login
    response_success_details['phone'] = user.i_user.phone if user.i_user else None
    response_success_details['email'] = user.i_user.email if user.i_user else user.t_user.email
    response_success_details['institutionName'] = user.get_health_facility().name if user.get_health_facility() else "",
    response_success_details['active'] = user.is_active
    response_success_details['dateCreated'] = user.validity_from
    return response_success_details
