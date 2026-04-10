
from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

# Wallet model for admin-configurable deposit addresses
class Wallet(models.Model):
    CRYPTO_CHOICES = [
        ('USDT', 'Tether (USDT)'),
        ('BTC', 'Bitcoin (BTC)'),
        ('ETH', 'Ethereum (ETH)'),
        ('BNB', 'BNB'),
        ('SOL', 'Solana (SOL)'),
    ]
    crypto_type = models.CharField(max_length=10, choices=CRYPTO_CHOICES, unique=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.get_crypto_type_display()} Wallet"

# UserNotification model for per-user notifications
class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.user.username}: {self.message[:40]}..."


class InvestmentPlan(models.Model):
    name = models.CharField(max_length=100)
    min_deposit = models.DecimalField(max_digits=12, decimal_places=2)
    max_deposit = models.DecimalField(max_digits=12, decimal_places=2)
    daily_profit_percent = models.DecimalField(max_digits=5, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    color_class = models.CharField(max_length=30, default='gold')
    icon = models.CharField(max_length=40, default='gem')
    badge = models.CharField(max_length=40, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'min_deposit']

    def __str__(self):
        return self.name

    def total_return_percent(self):
        return self.daily_profit_percent * self.duration_days


class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_broadcast = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
