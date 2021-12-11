import logging
from typing import Union

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from swish import SwishError

from foc_pay_web.focumama.forms import FocumamaForm
from foc_pay_web.payments.core import PaymentHandler

response = Union[HttpResponse, HttpResponseRedirect]

payment_handler = PaymentHandler(production=True)

logger = logging.getLogger(__name__)

def payment_form(request: HttpRequest) -> response:
    if request.method == "POST":
        form = FocumamaForm(request.POST)
        if form.is_valid():
            return _create_payment(request, raw_payer_alias=form.data["payer_alias"])
    else:
        form = FocumamaForm()
    return render(request, "focumama/form.html", {"form": form})

def _create_payment(request: HttpRequest, raw_payer_alias: str) -> response:
    payer_alias = int("46" + raw_payer_alias[1:])  # Replace 0 with 46

    try:
        payment = payment_handler.create_payment(
            payer_alias=payer_alias,
            amount=10,  # TODO: take from heroku config
        )

    except SwishError as e:
        logger.warning(e.error_message)
        form = FocumamaForm(request.POST)
        return render(request, "focumama/form.html", {"form": form})

    return HttpResponseRedirect(f"/payments/{payment.payment_id}", {"payment_id": payment.payment_id})
