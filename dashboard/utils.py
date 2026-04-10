from django.utils import timezone
from decimal import Decimal


def process_daily_profits(user=None):
    from .models import Investment
    from datetime import timedelta
    today = timezone.now().date()
    qs = Investment.objects.filter(status='active').select_related('plan','user__profile')
    if user:
        qs = qs.filter(user=user)
    for inv in qs:
        if inv.last_profit_date and inv.last_profit_date >= today:
            continue
        base = inv.last_profit_date or inv.start_date.date()
        days_due = (today - base).days
        if days_due <= 0:
            continue
        end_date = inv.start_date.date() + timedelta(days=inv.plan.duration_days)
        days_left_in_plan = (end_date - base).days
        days_to_credit = min(days_due, days_left_in_plan)
        if days_to_credit > 0:
            profit = inv.daily_profit() * days_to_credit
            _apply_profit(inv, profit)
        inv.last_profit_date = today
        inv.save(update_fields=['last_profit_date','profit_earned'])
        if today >= end_date:
            inv.status = 'completed'
            inv.end_date = timezone.now()
            inv.save(update_fields=['status','end_date'])


def _apply_profit(inv, profit):
    p = inv.user.profile
    inv.profit_earned += profit
    p.balance += profit
    p.total_profits += profit
    p.save(update_fields=['balance','total_profits'])


def award_referral_bonus(depositor):
    from .models import Deposit
    profile = depositor.profile
    if not profile.referred_by:
        return
    approved_count = Deposit.objects.filter(user=depositor, status='approved').count()
    if approved_count != 1:
        return
    first = Deposit.objects.filter(user=depositor, status='approved').first()
    if not first:
        return
    bonus = first.amount * Decimal('0.05')
    ref_profile = profile.referred_by.profile
    ref_profile.balance += bonus
    ref_profile.referral_bonus_earned += bonus
    ref_profile.save(update_fields=['balance','referral_bonus_earned'])
