from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
import random, string


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_deposited = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_profits = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_withdrawn = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    referral_bonus_earned = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    referral_code = models.CharField(max_length=12, unique=True, blank=True)
    referred_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – ${self.balance}"

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)

    def get_referral_link(self, request=None):
        path = f'/accounts/register/?ref={self.referral_code}'
        if request:
            return request.build_absolute_uri(path)
        return path


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
