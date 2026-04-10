from django.contrib import admin
from .models import Investment, Deposit, Withdrawal
admin.site.register(Investment)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
