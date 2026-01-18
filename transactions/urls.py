from django.urls import path
from .views import (
    withdraw,
    transfer,
    transaction_history,
)

urlpatterns = [
    path('withdraw/', withdraw, name='withdraw'),
    path('transfer/', transfer, name='transfer'),
    path('history/', transaction_history, name='transaction_history'),
]
