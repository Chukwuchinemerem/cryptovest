from django.contrib import admin
from .models import InvestmentPlan, Notification

@admin.register(InvestmentPlan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name','min_deposit','max_deposit','daily_profit_percent','duration_days','is_active','order']
    list_editable = ['is_active','order']

@admin.register(Notification)
class NotifAdmin(admin.ModelAdmin):
    list_display = ['title','is_broadcast','is_active','created_at']
