import logging
from typing import Union

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from swish import SwishError

from foc_pay_web.focumama.forms import FocumamaForm
from foc_pay_web.payments.core import PaymentHandler

response = Union[HttpResponse, HttpResponseRedirect]

logger = logging.getLogger(__name__)

payment_handler = PaymentHandler(production=True)


def payment_form(request: HttpRequest) -> response:
    if request.method == "POST":
        form = FocumamaForm(request.POST)
        if form.is_valid():
            payer_alias = int("46" + form.data["payer_alias"][1:])  # Replace 0 with 46
            try:
                payment = payment_handler.create_payment(
                    payer_alias=payer_alias,
                    amount=10,  # TODO: take from heroku config
                )
            except SwishError as e:
                logger.error(e.error_message)
                messages.add_message(request, messages.ERROR, e.error_message)
                form = FocumamaForm(request.POST)
                return render(request, "focumama/form.html", {"form": form})

            return redirect(f"/payments/{payment.payment_id}")

    else:
        form = FocumamaForm()

    return render(request, "focumama/form.html", {"form": form})
