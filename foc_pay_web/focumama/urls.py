from django.urls import path

from foc_pay_web.focumama.views import payment_form

app_name = "focumama"
urlpatterns = [
    path("", view=payment_form, name="payment_form"),
]
