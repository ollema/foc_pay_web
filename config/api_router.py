from django.conf import settings
from rest_framework.routers import DefaultRouter

from foc_pay_web.payments.api.views import PaymentViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = DefaultRouter()

# TODO: add user/account APIs when needed in the future
# router.register("users", UserViewSet)
router.register("payments", PaymentViewSet)

app_name = "api"
urlpatterns = router.urls
