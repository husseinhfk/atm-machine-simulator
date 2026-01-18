from django.contrib import admin
from .models import Transaction
from accounts.models import Account

# --- Account Admin ---
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "account_number", "balance")
    search_fields = ("user__username", "account_number")
    readonly_fields = ("account_number",)  # account number should not be editable

# --- Transaction Admin ---
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account", "transaction_type", "target_account", "amount", "timestamp")
    list_filter = ("transaction_type", "timestamp")
    search_fields = ("account__user__username", "target_account")
    ordering = ("-timestamp",)
