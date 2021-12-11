from typing import Union

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from swish import SwishError

from foc_pay_web.payments.core import PaymentHandler
from foc_pay_web.payments.models import Payment

response = Union[HttpResponse, HttpResponseRedirect]

payment_handler = PaymentHandler(production=True)


def test_view(request: HttpRequest) -> response:
    try:
        payment_handler.create_payment(
            payer_alias=46722338298,
            amount=10,
        )
    except SwishError as e:
        print(f"{e=}")
    return HttpResponseRedirect(f"/")
