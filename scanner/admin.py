from django.contrib import admin

from .models import StellarAccount, Payment, Badge


@admin.register(StellarAccount)
class StellarAccountAdmin(admin.ModelAdmin):
    list_display = [
        "account_id_identicon",
        "has_sq_badges",
        "badges",
        "nickname",
        "directory_tags",
        "suspect",
        "kosher",
    ]
    search_fields = ["public_key"]
    list_filter = ("suspect", "kosher", "has_sq_badges")

    class Media:
        css = {"all": ("admin/custom.css",)}


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["transaction_hash", "from_account_id_identicon", "to_account_id_identicon", "amount", "memo"]

    class Media:
        css = {"all": ("admin/custom.css",)}


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    pass
