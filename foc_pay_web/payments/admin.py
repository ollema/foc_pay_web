from django.contrib import admin

from foc_pay_web.payments.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ("payment_id",)
    fields = ("status", "status_changed", "payer_alias", "amount", "machine")

    list_display = readonly_fields + fields
    list_filter = ("status", "machine")
    ordering = ("-status_changed",)

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Payment, PaymentAdmin)
