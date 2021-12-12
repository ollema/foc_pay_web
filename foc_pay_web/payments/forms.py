from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class PaymentForm(forms.Form):
    phone_regex = RegexValidator(
        regex=r"^07\d{8}$",
        message=_("Telefonnumret måste ges i följande format: '07XXXXXXXX'"),
    )
    payer_alias = forms.CharField(
        label=_("Telefonnummer"),
        widget=forms.TextInput(attrs={"placeholder": "0712345678"}),
        validators=[phone_regex],
        max_length=20,
    )
