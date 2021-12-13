from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from foc_pay_web.payments.api.views import PaymentViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("payments", PaymentViewSet)

app_name = "api"
urlpatterns = router.urls
