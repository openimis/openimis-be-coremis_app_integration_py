from django.db.models import Q, Sum
from django.utils.translation import gettext_lazy as _
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
    FAILED,
    SUCCESS
)
from invoice.models import Bill
from payroll.models import (
    Payroll,
    PayrollStatus
)


ONSITE_PAYMENT = "StrategyOnSitePayment"
CHANNEL = "PPM"


@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
@permission_classes([IsAuthenticated])
def payment_details(request):
    channel = request.data.get('channel', None)
    if channel == CHANNEL:
        user = request.user
        payrolls = Payroll.objects.filter(
            payment_point__ppm=user,
            payment_method=ONSITE_PAYMENT,
            is_deleted=False,
            status=PayrollStatus.ONGOING
        )
        response_details = {}
        for payroll in payrolls:
            total_amount = _get_payroll_bills_amount(payroll)
            response_details[f'{payroll.name}'] = _build_success_output(total_amount)
        response_data = SUCCESS
        response_data["result"] = response_details
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response = FAILED
        response['result'] = _('Please provide PPM channel')
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


def _build_success_output(total_amount):
    response_payrolls = {
        'TOTAL_AMOUNT_PAID': 0.0,
        'TOTAL_AMOUNT_PAID_TO_PPM_BY_USER_EMAIL': None,
        'IS_RECONCILED': False,
        'TOTAL_AMOUNT_PAID_TO_PPM': None,
        'TOTAL_AMOUNT_PAID_TO_PPM_BY_USER': None,
        'TOTAL_AMOUNT': total_amount,
        'TOTAL_BENEFICIARY_PAID': 0
    }
    return response_payrolls


def _get_payroll_bills_amount(payroll):
    bills = _get_bill_attached_to_payroll(payroll)
    total_amount = str(bills.aggregate(total_amount=Sum('amount_total'))['total_amount'])
    return total_amount


def _get_bill_attached_to_payroll(payroll):
    filters = [Q(payrollbill__payroll_id=payroll.uuid,
                 is_deleted=False,
                 payrollbill__is_deleted=False,
                 payrollbill__payroll__is_deleted=False,
                 status=Bill.Status.VALIDATED)]
    bills = Bill.objects.filter(*filters)
    return bills
