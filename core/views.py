from django.shortcuts import render
from .models import InvestmentPlan, Notification

def landing(request):
    plans = InvestmentPlan.objects.filter(is_active=True).order_by('order')
    return render(request, 'core/landing.html', {'plans': plans})
