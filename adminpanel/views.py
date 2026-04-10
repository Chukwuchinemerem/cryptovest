from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from core.models import InvestmentPlan, Notification
from dashboard.models import Investment, Deposit, Withdrawal


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def admin_required(fn):
    return login_required(user_passes_test(is_admin, login_url='/accounts/login/')(fn))


@admin_required
def home(request):
    ctx = {
        'total_users': User.objects.filter(is_staff=False).count(),
        'total_deposits': Deposit.objects.filter(status='approved').aggregate(t=Sum('amount'))['t'] or 0,
        'total_withdrawals': Withdrawal.objects.filter(status='approved').aggregate(t=Sum('amount'))['t'] or 0,
        'active_investments': Investment.objects.filter(status='active').count(),
        'pending_deposits': Deposit.objects.filter(status='pending').count(),
        'pending_withdrawals': Withdrawal.objects.filter(status='pending').count(),
        'recent_users': User.objects.filter(is_staff=False).order_by('-date_joined')[:8],
    }
    return render(request, 'adminpanel/home.html', ctx)


@admin_required
def users(request):
    users_qs = User.objects.filter(is_staff=False).select_related('profile').order_by('-date_joined')
    return render(request, 'adminpanel/users.html', {'users': users_qs})


@admin_required
def user_detail(request, uid):
    u = get_object_or_404(User, id=uid)
    return render(request, 'adminpanel/user_detail.html', {
        'viewed_user': u,
        'investments': Investment.objects.filter(user=u).select_related('plan'),
        'deposits': Deposit.objects.filter(user=u),
        'withdrawals': Withdrawal.objects.filter(user=u),
    })


@admin_required
def deposits(request):
    return render(request, 'adminpanel/deposits.html', {
        'deposits': Deposit.objects.select_related('user').order_by('-created_at')
    })


@admin_required
def approve_deposit(request, did):
    dep = get_object_or_404(Deposit, id=did)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve' and dep.status == 'pending':
            dep.status = 'approved'
            dep.approved_at = timezone.now()
            dep.save()
            p = dep.user.profile
            p.balance += dep.amount
            p.total_deposited += dep.amount
            p.save(update_fields=['balance','total_deposited'])
            from dashboard.utils import award_referral_bonus
            award_referral_bonus(dep.user)
            messages.success(request, f'Deposit of ${dep.amount:,.2f} approved for {dep.user.username}.')
        elif action == 'reject' and dep.status == 'pending':
            dep.status = 'rejected'
            dep.save()
            messages.warning(request, 'Deposit rejected.')
    return redirect('adminpanel:deposits')


@admin_required
def withdrawals(request):
    return render(request, 'adminpanel/withdrawals.html', {
        'withdrawals': Withdrawal.objects.select_related('user').order_by('-created_at')
    })


@admin_required
def process_withdrawal(request, wid):
    wd = get_object_or_404(Withdrawal, id=wid)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve' and wd.status == 'pending':
            wd.status = 'approved'
            wd.processed_at = timezone.now()
            wd.save()
            messages.success(request, f'Withdrawal of ${wd.amount:,.2f} approved.')
        elif action == 'reject' and wd.status == 'pending':
            wd.status = 'rejected'
            wd.save()
            p = wd.user.profile
            p.balance += wd.amount
            p.total_withdrawn -= wd.amount
            p.save(update_fields=['balance','total_withdrawn'])
            messages.warning(request, 'Withdrawal rejected and amount refunded.')
    return redirect('adminpanel:withdrawals')


@admin_required
def plans(request):
    return render(request, 'adminpanel/plans.html', {
        'plans': InvestmentPlan.objects.all().order_by('order')
    })


@admin_required
def plan_create(request):
    if request.method == 'POST':
        try:
            InvestmentPlan.objects.create(
                name=request.POST['name'],
                min_deposit=Decimal(request.POST['min_deposit']),
                max_deposit=Decimal(request.POST['max_deposit']),
                daily_profit_percent=Decimal(request.POST['daily_profit_percent']),
                duration_days=int(request.POST['duration_days']),
                color_class=request.POST.get('color_class','gold'),
                icon=request.POST.get('icon','gem'),
                badge=request.POST.get('badge',''),
                order=int(request.POST.get('order',0)),
                is_active=request.POST.get('is_active') == 'on',
            )
            messages.success(request, '✅ Investment plan created!')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('adminpanel:plans')
    return render(request, 'adminpanel/plan_form.html', {'plan': None})


@admin_required
def plan_edit(request, pid):
    plan = get_object_or_404(InvestmentPlan, id=pid)
    if request.method == 'POST':
        try:
            plan.name = request.POST['name']
            plan.min_deposit = Decimal(request.POST['min_deposit'])
            plan.max_deposit = Decimal(request.POST['max_deposit'])
            plan.daily_profit_percent = Decimal(request.POST['daily_profit_percent'])
            plan.duration_days = int(request.POST['duration_days'])
            plan.color_class = request.POST.get('color_class','gold')
            plan.icon = request.POST.get('icon','gem')
            plan.badge = request.POST.get('badge','')
            plan.order = int(request.POST.get('order',0))
            plan.is_active = request.POST.get('is_active') == 'on'
            plan.save()
            messages.success(request, '✅ Plan updated!')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('adminpanel:plans')
    return render(request, 'adminpanel/plan_form.html', {'plan': plan})


@admin_required
def plan_delete(request, pid):
    plan = get_object_or_404(InvestmentPlan, id=pid)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Plan deleted.')
    return redirect('adminpanel:plans')


@admin_required
def notifications(request):
    if request.method == 'POST':
        Notification.objects.create(
            title=request.POST.get('title',''),
            message=request.POST.get('message',''),
            is_broadcast=True,
        )
        messages.success(request, '📢 Broadcast notification sent!')
        return redirect('adminpanel:notifications')
    return render(request, 'adminpanel/notifications.html', {
        'notifications': Notification.objects.all()
    })


@admin_required
def delete_notification(request, nid):
    notif = get_object_or_404(Notification, id=nid)
    if request.method == 'POST':
        notif.delete()
        messages.success(request, 'Notification deleted.')
    return redirect('adminpanel:notifications')
