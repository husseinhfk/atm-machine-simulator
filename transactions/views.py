from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction as db_transaction
from accounts.models import Account
from django.db.models import Sum, Q
from accounts.utils import verify_pin
from .models import Transaction
from decimal import Decimal

@login_required
def withdraw(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        amount = Decimal(request.POST.get("amount"))
        pin = request.POST.get("pin")

        if not verify_pin(request.user, pin):
            return render(request, "transactions/withdraw.html", {"error": "Invalid PIN"})

        if amount <= 0 or account.balance < amount:
            return render(request, "transactions/withdraw.html", {"error": "Invalid amount"})

        account.balance -= amount
        account.save()

        Transaction.objects.create(
            account=account,
            amount=amount,
            transaction_type="withdrawal"
        )

        return redirect("dashboard")
    
    context = {
        'quick_amounts': [20, 50, 100, 200, 500],
    }

    return render(request, "transactions/withdraw.html", context)


@login_required
def transfer(request):
    sender = Account.objects.get(user=request.user)

    if request.method == "POST":
        receiver_no = request.POST.get("recipient_account")
        amount = Decimal(request.POST.get("amount"))
        pin = request.POST.get("pin")

        if not verify_pin(request.user, pin):
            return render(request, "transactions/transfer.html", {"error": "Invalid PIN"})

        try:
            receiver = Account.objects.get(account_number=receiver_no)
        except Account.DoesNotExist:
            return render(request, "transactions/transfer.html", {"error": "Account not found"})

        if amount <= 0 or sender.balance < amount:
            return render(request, "transactions/transfer.html", {"error": "Insufficient funds"})

        with db_transaction.atomic():
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()

            Transaction.objects.create(
                account=sender,
                amount=amount,
                transaction_type="transfer",
                target_account=receiver.account_number
            )

        return redirect("dashboard")
    
    context = {
        'sender': sender, 
    }

    return render(request, "transactions/transfer.html", context)


@login_required
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by("-timestamp")

    balance = account.balance
    total_withdrawals = transactions.filter(transaction_type="withdrawal").aggregate(total=Sum("amount"))["total"] or 0
    total_transfers = transactions.filter(transaction_type="transfer").aggregate(total=Sum("amount"))["total"] or 0

    context = {
        "transactions": transactions,
        "balance": balance,
        "total_withdrawals": abs(total_withdrawals), 
        "total_transfers": abs(total_transfers),
    }
    return render(request, "transactions/history.html", context)
