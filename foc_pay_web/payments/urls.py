from django.urls import path
from django.views.generic.base import TemplateView

from foc_pay_web.payments.views import update_status

app_name = "payments"
urlpatterns = [
    path("<str:payment_id>", view=TemplateView.as_view(template_name="payments/status.html")),
    path("<str:payment_id>/update/", view=update_status),  # noqa
]
