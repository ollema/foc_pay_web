import swish
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse

from foc_pay_web.payments.models import Payment

SWISH_NUMBER = "1230814343"
CERT_PATH = (".certs/prod/cert.pem", ".certs/prod/swish.key")
CURRENCY = "SEK"
MESSAGE = "GET HIPPER WITH FLIPPER."


class PaymentHandler:
    def __init__(self) -> None:
        self.client = swish.SwishClient("production", SWISH_NUMBER, CERT_PATH, True)

    def create_payment(
        self,
        payer_alias: int,
        amount: int,
        machine_name: str,
    ) -> Payment:
        debug_callback_url = "https://google.com"
        callback_url = f"https://{settings.ALLOWED_HOSTS[0]}{reverse('payments:swish_callback')}"
        callback_url = debug_callback_url if settings.DEBUG else callback_url

        swish_payment = self.client.create_payment(
            amount=amount,
            currency=CURRENCY,
            callback_url=callback_url,
            message=MESSAGE,
            payer_alias=payer_alias,
        )
        swish_payment = self.client.get_payment(payment_request_id=swish_payment.id)

        return Payment.objects.create(
            payment_id=swish_payment.id,
            payer_alias=swish_payment.payer_alias,
            amount=swish_payment.amount,
            machine=machine_name,
        )

    def update_payment_status(
        self,
        payment_id: str,
    ) -> None:
        database_payment: Payment = get_object_or_404(Payment, pk=payment_id)
        swish_payment = self.client.get_payment(payment_request_id=payment_id)

        # don't update payment status in db if payment has been credited already
        if database_payment.status != Payment.STATUS.credited:
            # don't update payment status in db if no update is needed
            if swish_payment.status.lower() != database_payment.status:
                if swish_payment.status == "PAID":
                    database_payment.status = Payment.STATUS.paid
                elif swish_payment.status == "DECLINED":
                    database_payment.status = Payment.STATUS.declined
                elif swish_payment.status == "ERROR":
                    database_payment.status = Payment.STATUS.error
                elif swish_payment.status == "CANCELLED":
                    database_payment.status = Payment.STATUS.cancelled

                database_payment.save()
