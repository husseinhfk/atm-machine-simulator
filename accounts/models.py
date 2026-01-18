from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import random

def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True, default=generate_account_number)
    pin = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin)

    def __str__(self):
        return self.account_number
