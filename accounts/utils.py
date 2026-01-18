from .models import Account

def verify_pin(user, pin):
    account = Account.objects.get(user=user)
    return account.check_pin(pin)
