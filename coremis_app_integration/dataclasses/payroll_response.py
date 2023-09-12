from dataclasses import dataclass


@dataclass
class PayrollResponse:
    TOTAL_AMOUNT_PAID: float = 0.0
    TOTAL_AMOUNT_PAID_TO_PPM_BY_USER_EMAIL: float = None
    IS_RECONCILED: bool = False
    TOTAL_AMOUNT_PAID_TO_PPM: float = None
    TOTAL_AMOUNT_PAID_TO_PPM_BY_USER: float = None
    TOTAL_AMOUNT: float = 0
    TOTAL_BENEFICIARY_PAID: float = 0
