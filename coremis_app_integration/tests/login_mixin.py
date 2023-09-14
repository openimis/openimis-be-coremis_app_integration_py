from core.forms import User
from core.services import (
    create_or_update_interactive_user,
    create_or_update_core_user
)
from coremis_app_integration.utils import DbManagerUtils
from location.models import Location
from payroll.models import PaymentPoint



class LogInMixin:
    _TEST_USER_NAME = "TestUserTest2"
    _TEST_USER_PASSWORD = "TestPasswordTest2"
    _TEST_DATA_USER = {
        "username": _TEST_USER_NAME,
        "last_name": _TEST_USER_NAME,
        "password": _TEST_USER_PASSWORD,
        "other_names": _TEST_USER_NAME,
        "user_types": "INTERACTIVE",
        "language": "en",
        "roles": [1, 3, 5, 9],
    }

    def get_or_create_user_api(self):
        user = DbManagerUtils.get_object_or_none(User, username=self._TEST_USER_NAME)
        if user is None:
            user = self.__create_user_interactive_core()
        return user

    def __create_user_interactive_core(self):
        i_user, i_user_created = create_or_update_interactive_user(
            user_id=None, data=self._TEST_DATA_USER, audit_user_id=999, connected=False)
        create_or_update_core_user(
            user_uuid=None, username=self._TEST_DATA_USER["username"], i_user=i_user)
        user = DbManagerUtils.get_object_or_none(User, username=self._TEST_USER_NAME)
        self.__create_payment_point(user)
        return user

    def __create_payment_point(self, user, **kwargs):
        name = "TestPPM",
        location = Location.objects.filter(validity_to__isnull=True, type='V').first()
        payment_point = PaymentPoint(
            name=name,
            location=location,
            ppm=user
        )
        payment_point.save(username=user.username)
        return payment_point
