from django.db import models
from decimal import Decimal


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
