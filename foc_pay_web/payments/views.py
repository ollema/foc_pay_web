import logging
from typing import Union

from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from swish import SwishError

from foc_pay_web.payments.core import PaymentHandler
from foc_pay_web.payments.forms import PaymentForm
from foc_pay_web.payments.models import Payment

response = Union[HttpResponse, HttpResponseRedirect]

logger = logging.getLogger(__name__)

payment_handler = PaymentHandler(production=True)


def _payment_form(request: HttpRequest, machine_name: str) -> response:
    if request.method == "POST":
        form = PaymentForm(request.POST)
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
                form = PaymentForm(request.POST)
                return render(
                    request,
                    "payments/payment_form.html",
                    context={"form": form, "machine_name": machine_name},
                )

            return redirect(f"/payments/{payment.payment_id}")

    else:
        form = PaymentForm()

    return render(
        request,
        "payments/payment_form.html",
        context={"form": form, "machine_name": machine_name},
    )


def focumama_payment_form(request: HttpRequest) -> response:
    return _payment_form(request, machine_name="Focumama")


def drickomaten_payment_form(request: HttpRequest) -> response:
    return _payment_form(request, machine_name="Drickomaten")


def get_payment(request: HttpRequest, payment_id: str) -> response:
    return render(request, "payments/payment.html", context={"payment_id": payment_id})


def update_payment_status(request: HttpRequest, payment_id: str) -> response:
    payment_handler.update_payment_status(payment_id)
    payment = get_object_or_404(Payment, pk=payment_id)
    return render(request, "payments/payment_status.html", context={"payment": payment})
