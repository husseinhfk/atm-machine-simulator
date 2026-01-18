from django.db import models
from accounts.models import Account

class Transaction(models.Model):
    TYPES = (
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    target_account = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
