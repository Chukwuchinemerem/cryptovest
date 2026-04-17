from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_view, name='notifications'),
    path('mark-read/<int:pk>/', views.mark_read, name='mark_notification_read'),
]
