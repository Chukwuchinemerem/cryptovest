from django.db import models
from django.contrib.auth.models import User
from core.models import InvestmentPlan
from decimal import Decimal
from django.utils import timezone


class Investment(models.Model):
    STATUS = [('active','Active'),('completed','Completed'),('cancelled','Cancelled')]
    CRYPTO = [('BTC','Bitcoin (BTC)'),('ETH','Ethereum (ETH)'),('USDT','Tether (USDT)'),('BNB','BNB'),('SOL','Solana (SOL)')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    profit_earned = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    last_profit_date = models.DateField(null=True, blank=True)
    class Meta:
        ordering = ['-start_date']
    def __str__(self):
        return f"{self.user.username} – {self.plan.name} – ${self.amount}"
    def daily_profit(self):
        return self.amount * (self.plan.daily_profit_percent / Decimal('100'))
    def expected_end_date(self):
        from datetime import timedelta
        return self.start_date + timedelta(days=self.plan.duration_days)
    def days_remaining(self):
        d = (self.expected_end_date() - timezone.now()).days
        return max(0, d)
    def total_expected_profit(self):
        v = self.amount * (self.plan.daily_profit_percent / Decimal('100')) * self.plan.duration_days
        return v if v > 0 else Decimal('1')
    def progress_percent(self):
        return min(100, int((self.profit_earned / self.total_expected_profit()) * 100))


class Deposit(models.Model):
    STATUS = [('pending','Pending'),('approved','Approved'),('rejected','Rejected')]
    CRYPTO = [('BTC','Bitcoin (BTC)'),('ETH','Ethereum (ETH)'),('USDT','Tether (USDT)'),('BNB','BNB'),('SOL','Solana (SOL)')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    crypto_type = models.CharField(max_length=10, choices=CRYPTO, default='USDT')
    transaction_hash = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.user.username} – ${self.amount} – {self.status}"


class Withdrawal(models.Model):
    STATUS = [('pending','Pending'),('approved','Approved'),('rejected','Rejected')]
    CRYPTO = [('BTC','Bitcoin (BTC)'),('ETH','Ethereum (ETH)'),('USDT','Tether (USDT)'),('BNB','BNB'),('SOL','Solana (SOL)')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    crypto_type = models.CharField(max_length=10, choices=CRYPTO, default='USDT')
    wallet_address = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.user.username} – ${self.amount} – {self.status}"
