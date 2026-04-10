from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='InvestmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('min_deposit', models.DecimalField(decimal_places=2, max_digits=12)),
                ('max_deposit', models.DecimalField(decimal_places=2, max_digits=12)),
                ('daily_profit_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('duration_days', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('color_class', models.CharField(default='gold', max_length=30)),
                ('icon', models.CharField(default='gem', max_length=40)),
                ('badge', models.CharField(blank=True, max_length=40)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'min_deposit']},
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('is_broadcast', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
