import swish
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate

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
    ) -> Payment:
        payment = self.client.create_payment(
            amount=amount,
            currency=CURRENCY,
            callback_url="https://google.com",
            message=MESSAGE,
            payer_alias=payer_alias,
        )
        payment = self.client.get_payment(payment_request_id=payment.id)

        Payment.objects.create(
            payment_id=payment.id,
            payer_alias=int(payment.payer_alias),
            amount=int(payment.amount),
        )

    def update_payment_status(
        self,
        payment_id: str,
    ) -> bool:
        pass
