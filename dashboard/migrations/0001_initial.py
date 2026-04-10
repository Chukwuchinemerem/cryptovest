from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('auth','0012_alter_user_first_name_max_length'),('core','0001_initial')]
    operations = [
        migrations.CreateModel('Investment', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
            ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
            ('profit_earned', models.DecimalField(decimal_places=2, default='0.00', max_digits=15)),
            ('status', models.CharField(choices=[('active','Active'),('completed','Completed'),('cancelled','Cancelled')], default='active', max_length=20)),
            ('start_date', models.DateTimeField(auto_now_add=True)),
            ('end_date', models.DateTimeField(blank=True, null=True)),
            ('last_profit_date', models.DateField(blank=True, null=True)),
            ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.investmentplan')),
            ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='auth.user')),
        ], options={'ordering': ['-start_date']}),
        migrations.CreateModel('Deposit', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
            ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
            ('crypto_type', models.CharField(choices=[('BTC','Bitcoin'),('ETH','Ethereum'),('USDT','Tether'),('BNB','BNB'),('SOL','Solana')], default='USDT', max_length=10)),
            ('transaction_hash', models.CharField(blank=True, max_length=200)),
            ('status', models.CharField(choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending', max_length=20)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('approved_at', models.DateTimeField(blank=True, null=True)),
            ('notes', models.TextField(blank=True)),
            ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to='auth.user')),
        ], options={'ordering': ['-created_at']}),
        migrations.CreateModel('Withdrawal', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
            ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
            ('crypto_type', models.CharField(choices=[('BTC','Bitcoin'),('ETH','Ethereum'),('USDT','Tether'),('BNB','BNB'),('SOL','Solana')], default='USDT', max_length=10)),
            ('wallet_address', models.CharField(max_length=200)),
            ('status', models.CharField(choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending', max_length=20)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('processed_at', models.DateTimeField(blank=True, null=True)),
            ('notes', models.TextField(blank=True)),
            ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawals', to='auth.user')),
        ], options={'ordering': ['-created_at']}),
    ]
