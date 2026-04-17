from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_users, name='admin_users'),
    path('users/<int:pk>/', views.admin_user_detail, name='admin_user_detail'),
    path('deposits/', views.admin_deposits, name='admin_deposits'),
    path('withdrawals/', views.admin_withdrawals, name='admin_withdrawals'),
    path('investments/', views.admin_investments, name='admin_investments'),
    path('plans/', views.admin_plans, name='admin_plans'),
    path('wallets/', views.admin_wallets, name='admin_wallets'),
    path('content/', views.admin_content, name='admin_content'),
    path('process-profits/', views.admin_process_profits, name='admin_process_profits'),
]
