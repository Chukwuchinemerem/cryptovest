from django.urls import path
from . import views
app_name = 'adminpanel'
urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('users/<int:uid>/', views.user_detail, name='user_detail'),
    path('deposits/', views.deposits, name='deposits'),
    path('deposits/<int:did>/action/', views.approve_deposit, name='approve_deposit'),
    path('withdrawals/', views.withdrawals, name='withdrawals'),
    path('withdrawals/<int:wid>/action/', views.process_withdrawal, name='process_withdrawal'),
    path('plans/', views.plans, name='plans'),
    path('plans/create/', views.plan_create, name='plan_create'),
    path('plans/<int:pid>/edit/', views.plan_edit, name='plan_edit'),
    path('plans/<int:pid>/delete/', views.plan_delete, name='plan_delete'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:nid>/delete/', views.delete_notification, name='delete_notification'),
    # New admin features:
    path('add-funds/', views.add_funds, name='add_funds'),
    path('wallet-settings/', views.wallet_settings, name='wallet_settings'),
]
