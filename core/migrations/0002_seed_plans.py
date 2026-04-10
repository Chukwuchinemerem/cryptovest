from django.db import migrations

def seed_plans(apps, schema_editor):
    Plan = apps.get_model('core', 'InvestmentPlan')
    plans = [
        dict(name='Starter',  min_deposit=50,    max_deposit=999,    daily_profit_percent='1.50', duration_days=7,  color_class='bronze',   icon='seedling',   badge='',         order=1),
        dict(name='Silver',   min_deposit=1000,  max_deposit=4999,   daily_profit_percent='2.50', duration_days=14, color_class='silver',   icon='chart-line', badge='',         order=2),
        dict(name='Gold',     min_deposit=5000,  max_deposit=19999,  daily_profit_percent='3.50', duration_days=21, color_class='gold',     icon='coins',      badge='Popular',  order=3),
        dict(name='Platinum', min_deposit=20000, max_deposit=49999,  daily_profit_percent='5.00', duration_days=30, color_class='platinum', icon='gem',        badge='Best ROI', order=4),
        dict(name='Diamond',  min_deposit=50000, max_deposit=500000, daily_profit_percent='7.50', duration_days=30, color_class='diamond',  icon='crown',      badge='VIP',      order=5),
    ]
    for p in plans:
        Plan.objects.get_or_create(name=p['name'], defaults=p)

class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]
    operations = [migrations.RunPython(seed_plans, migrations.RunPython.noop)]
