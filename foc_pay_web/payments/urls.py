from django.urls import path

from foc_pay_web.payments.views import get_payment, swish_callback, update_payment_status

app_name = "payments"
urlpatterns = [
    path("swish_callback", view=swish_callback, name="swish_callback"),
    path("<str:payment_id>", view=get_payment),
    path("<str:payment_id>/update/", view=update_payment_status),
]
