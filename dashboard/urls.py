from django.urls import path
from . import views
app_name = 'dashboard'
urlpatterns = [
    path('', views.home, name='home'),
    path('invest/', views.invest, name='invest'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transactions/', views.transactions, name='transactions'),
    path('referral/', views.referral, name='referral'),
    path('notifications/', views.notifications, name='notifications'),
]
