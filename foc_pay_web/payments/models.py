from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import StatusModel


class Payment(StatusModel):
    STATUS = Choices(
        ("created", _("Created")),
        ("paid", _("Paid")),
        ("credited", _("Credited")),
        ("declined", _("Declined")),
        ("error", _("Error")),
        ("cancelled", _("Cancelled")),
    )

    payment_id = models.CharField(max_length=100, primary_key=True)
    payer_alias = models.CharField(max_length=20)
    amount = models.CharField(max_length=10)
