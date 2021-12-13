import json
from typing import Dict, Union

from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import (
    Http404,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from swish import SwishError

from foc_pay_web.payments.core import PaymentHandler
from foc_pay_web.payments.forms import PaymentForm
from foc_pay_web.payments.models import Payment

response = Union[HttpResponse, HttpResponseRedirect]

payment_handler = PaymentHandler()


def _payment_form(
    request: HttpRequest,
    price: int,
    machine_name: str,
    page_content: Dict[str, str],
) -> response:
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                payment = payment_handler.create_payment(
                    payer_alias=int("46" + form.data["payer_alias"][1:]),  # Replace 0 with 46
                    amount=price,
                    machine_name=machine_name,
                )
            except SwishError as e:
                messages.add_message(request, messages.ERROR, e.error_message)
                form = PaymentForm(request.POST)
                return render(
                    request,
                    "payments/payment_form.html",
                    context={
                        "form": form,
                        "page_content": page_content,
                    },
                )

            return redirect(f"/payments/{payment.payment_id}")
    else:
        form = PaymentForm()

    return render(
        request,
        "payments/payment_form.html",
        context={
            "form": form,
            "page_content": page_content,
        },
    )


def focumama_payment_form(request: HttpRequest) -> response:
    price = 10
    machine_name = Payment.MACHINES.focumama
    page_content = {
        "title": _("Focumama"),
        "help_text": [
            _("Enter your phone number and open Swish."),
            _("When your payment has been processed you are free to select an item from the machine."),
        ],
    }
    return _payment_form(request, price=price, machine_name=machine_name, page_content=page_content)


def drickomaten_payment_form(request: HttpRequest) -> response:
    price = 8
    machine_name = Payment.MACHINES.drickomaten
    page_content = {
        "title": _("Drickomaten"),
        "help_text": [
            _("Enter your phone number and open Swish."),
            _("When your payment has been processed you are free to select a soda from the machine."),
        ],
    }
    return _payment_form(request, price=price, machine_name=machine_name, page_content=page_content)


def focumama_free_vend_form(request: HttpRequest) -> response:
    price = 1
    machine_name = Payment.MACHINES.focumama
    page_content = {
        "title": _("Period products"),
        "help_text": [
            _(
                "With the help of a simple trick you can acquire free period products from Focumama "
                "(while supplies last)."
            ),
            _("Enter your phone number and open Swish."),
            _("<b>IMPORTANT!</b> Do not accept the payment request in Swish - decline it instead!"),
            _(
                "When your payment request has been processed you are free to select from slot EO or "
                "slot E1 in Focumama."
            ),
        ],
    }
    return _payment_form(request, price=price, machine_name=machine_name, page_content=page_content)


def payment(request: HttpRequest, payment_id: str) -> response:
    return render(request, "payments/payment.html", context={"payment_id": payment_id})


def update_payment_status(request: HttpRequest, payment_id: str) -> response:
    try:
        payment_handler.update_payment_status(payment_id)
        payment = Payment.objects.get(pk=payment_id)
        return render(request, "payments/payment_status.html", context={"payment": payment})
    except Http404:
        return HttpResponseNotFound()


@csrf_exempt
def swish_callback(request: HttpRequest) -> response:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    payment = json.loads(request.body)
    update_payment_status(request, payment_id=payment["id"])
    return HttpResponse("OK")
