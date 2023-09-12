"""
Provides various authentication policies.
"""
import base64
import binascii

from dataclasses import asdict
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import (
    authenticate,
    BasicAuthentication,
    get_authorization_header
)

from rest_framework import exceptions
from coremis_app_integration.dataclasses import FailedResponse


class CustomBasicAuthentication(BasicAuthentication):
    """
    HTTP Basic authentication against username/password.
    """
    def _authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth = get_authorization_header(request).split()

        if not auth or not self.__is_basic_auth(auth):
            return None

        if len(auth) == 1:
            response = FailedResponse()
            response.result = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(asdict(response))
        elif len(auth) > 2:
            response = FailedResponse()
            response.result = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(asdict(response))

        try:
            try:
                auth_decoded = base64.b64decode(auth[1]).decode('utf-8')
            except UnicodeDecodeError:
                auth_decoded = base64.b64decode(auth[1]).decode('latin-1')
            auth_parts = auth_decoded.partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            response = FailedResponse()
            response.result = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(asdict(response))

        userid, password = auth_parts[0], auth_parts[2]
        return self.authenticate_credentials(userid, password, request)

    def __is_basic_auth(self, auth_header):
        return auth_header.lower().startswith(b'basic')

    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        credentials = {
            get_user_model().USERNAME_FIELD: userid,
            'password': password
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            response = FailedResponse()
            response.result = _('Invalid username/password.')
            raise exceptions.AuthenticationFailed(asdict(response))

        if not user.is_active:
            response = FailedResponse()
            response.result = _('User inactive or deleted.')
            raise exceptions.AuthenticationFailed(asdict(response))

        return user, None
