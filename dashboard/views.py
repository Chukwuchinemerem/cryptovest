
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from .models import Investment, Deposit, Withdrawal
from core.models import InvestmentPlan, Notification
from .utils import process_daily_profits

@login_required
def notifications(request):
    from core.models import UserNotification
    notes = UserNotification.objects.filter(user=request.user).order_by('-created_at')
    if request.GET.get('ajax') == '1':
        from django.http import JsonResponse
        latest = notes.first()
        return JsonResponse({
            'latest': {
                'id': latest.id if latest else None,
                'message': latest.message if latest else '',
                'created_at': latest.created_at.isoformat() if latest else '',
            } if latest else None
        })
    return render(request, 'dashboard/notifications.html', {'notifications': notes})


@login_required
def home(request):
    process_daily_profits(request.user)
    profile = getattr(request.user, 'profile', None)
    if profile is None:
        from accounts.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
    active_investments = Investment.objects.filter(user=request.user, status='active').select_related('plan')
    recent_deposits = Deposit.objects.filter(user=request.user)[:5]
    recent_withdrawals = Withdrawal.objects.filter(user=request.user)[:5]
    notifications = Notification.objects.filter(is_active=True, is_broadcast=True)[:5]
    return render(request, 'dashboard/home.html', {
        'profile': profile,
        'active_investments': active_investments,
        'recent_deposits': recent_deposits,
        'recent_withdrawals': recent_withdrawals,
        'notifications': notifications,
        'active_count': active_investments.count(),
        'referral_link': profile.get_referral_link(request),
        'referral_count': request.user.referrals.count(),
    })


@login_required
def invest(request):
    plans = InvestmentPlan.objects.filter(is_active=True).order_by('order')
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        try:
            amount = Decimal(request.POST.get('amount','0'))
        except InvalidOperation:
            messages.error(request, 'Invalid amount.')
            return redirect('dashboard:invest')
        plan = get_object_or_404(InvestmentPlan, id=plan_id, is_active=True)
        profile = getattr(request.user, 'profile', None)
        if profile is None:
            from accounts.models import UserProfile
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if amount < plan.min_deposit:
            messages.error(request, f'Minimum for {plan.name} is ${plan.min_deposit:,.2f}.')
            return redirect('dashboard:invest')
        if amount > plan.max_deposit:
            messages.error(request, f'Maximum for {plan.name} is ${plan.max_deposit:,.2f}.')
            return redirect('dashboard:invest')
        if profile.balance < amount:
            messages.error(request, 'Insufficient balance. Please deposit first.')
            return redirect('dashboard:deposit')
        profile.balance -= amount
        profile.save(update_fields=['balance'])
        Investment.objects.create(user=request.user, plan=plan, amount=amount, last_profit_date=timezone.now().date())
        messages.success(request, f'🚀 Invested ${amount:,.2f} in {plan.name} Plan! Daily profits start accruing now.')
        return redirect('dashboard:home')
    return render(request, 'dashboard/invest.html', {'plans': plans})


@login_required
def deposit(request):
    from core.models import Wallet
    CRYPTO_ADDRESSES = {w.crypto_type: w.address for w in Wallet.objects.all()}
    profile = getattr(request.user, 'profile', None)
    if profile is None:
        from accounts.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount','0'))
            if amount <= 0: raise ValueError()
        except (InvalidOperation, ValueError):
            messages.error(request, 'Enter a valid amount.')
            return redirect('dashboard:deposit')
        dep = Deposit.objects.create(
            user=request.user,
            amount=amount,
            crypto_type=request.POST.get('crypto_type','USDT'),
            transaction_hash=request.POST.get('transaction_hash','').strip(),
        )
        # Create notification for deposit submitted
        from core.models import UserNotification
        UserNotification.objects.create(user=request.user, message=f'Your deposit of ${amount:,.2f} has been submitted and is pending review.')
        messages.success(request, f'✅ Deposit of ${amount:,.2f} submitted! You will be credited after admin review (1–3 hrs).')
        return redirect('dashboard:home')
    return render(request, 'dashboard/deposit.html', {'crypto_addresses': CRYPTO_ADDRESSES})


@login_required
def withdraw(request):
    profile = getattr(request.user, 'profile', None)
    if profile is None:
        from accounts.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount','0'))
            if amount <= 0: raise ValueError()
        except (InvalidOperation, ValueError):
            messages.error(request, 'Enter a valid amount.')
            return redirect('dashboard:withdraw')
        wallet = request.POST.get('wallet_address','').strip()
        if amount < Decimal('10'):
            messages.error(request, 'Minimum withdrawal is $10.')
            return redirect('dashboard:withdraw')
        if amount > profile.balance:
            messages.error(request, f'Insufficient balance. Available: ${profile.balance:,.2f}')
            return redirect('dashboard:withdraw')
        if not wallet:
            messages.error(request, 'Wallet address is required.')
            return redirect('dashboard:withdraw')
        profile.balance -= amount
        profile.total_withdrawn += amount
        profile.save(update_fields=['balance','total_withdrawn'])
        Withdrawal.objects.create(
            user=request.user, amount=amount,
            crypto_type=request.POST.get('crypto_type','USDT'),
            wallet_address=wallet,
        )
        messages.success(request, f'💸 Withdrawal of ${amount:,.2f} requested! Processing within 24 hours.')
        return redirect('dashboard:home')
    return render(request, 'dashboard/withdraw.html', {'profile': profile})


@login_required
def transactions(request):
    return render(request, 'dashboard/transactions.html', {
        'deposits': Deposit.objects.filter(user=request.user),
        'withdrawals': Withdrawal.objects.filter(user=request.user),
        'investments': Investment.objects.filter(user=request.user).select_related('plan'),
    })


@login_required
def referral(request):
    profile = getattr(request.user, 'profile', None)
    if profile is None:
        from accounts.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
    referrals = request.user.referrals.select_related('user').all()
    return render(request, 'dashboard/referral.html', {
        'profile': profile,
        'referral_link': profile.get_referral_link(request),
        'referrals': referrals,
    })
