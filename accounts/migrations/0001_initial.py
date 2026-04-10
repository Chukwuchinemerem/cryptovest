from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('auth','0012_alter_user_first_name_max_length')]
    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default='0.00', max_digits=15)),
                ('total_deposited', models.DecimalField(decimal_places=2, default='0.00', max_digits=15)),
                ('total_profits', models.DecimalField(decimal_places=2, default='0.00', max_digits=15)),
                ('total_withdrawn', models.DecimalField(decimal_places=2, default='0.00', max_digits=15)),
                ('referral_bonus_earned', models.DecimalField(decimal_places=2, default='0.00', max_digits=12)),
                ('referral_code', models.CharField(blank=True, max_length=12, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('referred_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referrals', to='auth.user')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
        ),
    ]
