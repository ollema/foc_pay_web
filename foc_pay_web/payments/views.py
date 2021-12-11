import logging
from typing import Union

from django.core.exceptions import ObjectDoesNotExist
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from foc_pay_web.payments.core import PaymentHandler
from foc_pay_web.payments.models import Payment

response = Union[HttpResponse, HttpResponseRedirect]

payment_handler = PaymentHandler(production=True)

logger = logging.getLogger(__name__)


def update_status(request: HttpRequest, payment_id: str) -> response:

    payment_handler.update_payment_status(payment_id)

    database_payment = None

    try:
        database_payment: Payment = Payment.objects.get(pk=payment_id)

    except ObjectDoesNotExist:
        print(f"error: was asked to update {payment_id} but could not find it in db")

    return render(request, "payments/swish_payment_status.html", context={"payment": database_payment})
