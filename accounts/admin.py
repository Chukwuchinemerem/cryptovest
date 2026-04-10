from django.contrib import admin
from .models import UserProfile
@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','balance','total_deposited','total_profits','referral_code']
    search_fields = ['user__username','user__email']
