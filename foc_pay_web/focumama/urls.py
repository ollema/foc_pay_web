from django.urls import path

from foc_pay_web.focumama.views import test_view

app_name = "focumama"
urlpatterns = [
    path("", view=test_view),
]
