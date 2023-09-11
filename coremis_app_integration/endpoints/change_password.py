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


@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    old_password = request.data.get('oldpassword', None)
    new_password = request.data.get('newpassword', None)
    confirm_password = request.data.get('confirmpassword', None)
    user = request.user
    authenticated_user = authenticate(username=user.username, password=old_password)
    if authenticated_user:
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            response_data = SUCCESS
            response_data["result"] = {}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response = FAILED
            response['result'] = _('The new password does not match the confirmation of new one')
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    else:
        response = FAILED
        response['result'] = _('Please provide correct old password')
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


def _build_success_output(user):
    pass
