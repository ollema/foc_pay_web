from rest_framework import serializers

from foc_pay_web.payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("payment_id", "status", "status_changed", "payer_alias", "amount", "machine")
