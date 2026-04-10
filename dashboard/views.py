from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from .models import Investment, Deposit, Withdrawal
from core.models import InvestmentPlan, Notification
from .utils import process_daily_profits


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
    CRYPTO_ADDRESSES = {
        'BTC':  '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        'ETH':  '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'USDT': 'TYourUSDTTRC20AddressHere',
        'BNB':  'bnb1grpf0955h0ykzq3ar5nmum7y6gdfl6lxfn46h2',
        'SOL':  'YourSolanaAddressHere',
    }
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
        Deposit.objects.create(
            user=request.user,
            amount=amount,
            crypto_type=request.POST.get('crypto_type','USDT'),
            transaction_hash=request.POST.get('transaction_hash','').strip(),
        )
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
