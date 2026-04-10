from django.contrib import admin
from .models import InvestmentPlan, Notification, Wallet, UserNotification

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['crypto_type', 'address']
    list_editable = ['address']

@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']

@admin.register(InvestmentPlan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name','min_deposit','max_deposit','daily_profit_percent','duration_days','is_active','order']
    list_editable = ['is_active','order']

@admin.register(Notification)
class NotifAdmin(admin.ModelAdmin):
    list_display = ['title','is_broadcast','is_active','created_at']
