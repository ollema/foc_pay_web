import swish
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse

from foc_pay_web.payments.models import Payment

CURRENCY = "SEK"
MESSAGE = "GET HIPPER WITH FLIPPER. GET LOOSE WITH BOOZE"


swish_prod_client = swish.SwishClient(
    environment=swish.Environment.Production,
    merchant_swish_number="1230814343",
    cert=(".certs/prod/cert.pem", ".certs/prod/swish.key"),
    verify=True,
)

swish_test_client = swish.SwishClient(
    environment=swish.Environment.Test,
    merchant_swish_number="1231181189",
    cert=(".certs/test/cert.pem", ".certs/test/swish.key"),
)


class PaymentHandler:
    def __init__(self, production: bool = False) -> None:
        if production:
            self.client = swish_prod_client
        else:
            self.client = swish_test_client

    def create_payment(
        self,
        payer_alias: int,
        amount: int,
        machine_name: str,
    ) -> Payment:
        debug_callback_url = "https://google.com"
        prod_callback_url = f"https://{settings.ALLOWED_HOSTS[0]}{reverse('payments:swish_callback')}"
        callback_url = debug_callback_url if settings.DEBUG else prod_callback_url
        print(f"{callback_url=}")

        payment = self.client.create_payment(
            amount=amount,
            currency=CURRENCY,
            callback_url=callback_url,
            message=MESSAGE,
            payer_alias=payer_alias,
        )
        payment = self.client.get_payment(payment_request_id=payment.id)

        return Payment.objects.create(
            payment_id=payment.id,
            payer_alias=int(payment.payer_alias),
            amount=int(payment.amount),
            machine=machine_name,
        )

    def update_payment_status(
        self,
        payment_id: str,
    ) -> None:
        database_payment: Payment = get_object_or_404(Payment, pk=payment_id)
        swish_payment = self.client.get_payment(payment_request_id=payment_id)

        # never update payment status if it has been credited once
        if not database_payment.status == Payment.STATUS.credited:
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
