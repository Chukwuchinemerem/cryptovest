from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import UserProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    ref_code = request.GET.get('ref','')
    referrer = None
    if ref_code:
        try:
            referrer = UserProfile.objects.get(referral_code=ref_code).user
        except UserProfile.DoesNotExist:
            pass
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        rc = request.POST.get('ref_code','')
        if rc and not referrer:
            try:
                referrer = UserProfile.objects.get(referral_code=rc).user
            except UserProfile.DoesNotExist:
                pass
        if form.is_valid():
            user = form.save(commit=True, referrer=referrer)
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Account created successfully.')
            return redirect('dashboard:home')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form, 'ref_code': ref_code, 'referrer': referrer})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get('next','') or 'dashboard:home')
        messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out safely.')
    return redirect('core:landing')
