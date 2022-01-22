from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from foc_pay_web.payments.models import Payment


class PaymentForm(forms.Form):
    phone_regex = RegexValidator(
        regex=r"^07\d{8}$",
        message=_("Enter your phone number using this format: '07XXXXXXXX'"),
    )
    payer_alias = forms.CharField(
        label=_("Phone number"),
        widget=forms.TextInput(attrs={"placeholder": "0712345678"}),
        validators=[phone_regex],
        max_length=20,
    )

    def clean(self):
        paid_focumama_payment = Payment.paid.filter(machine=Payment.MACHINES.focumama).first()
        if paid_focumama_payment:
            raise ValidationError(
                _(
                    "Another payment is already in progress!"
                    "Contact Foc (foc@ftek.se) if the machine is not responding."
                )
            )
