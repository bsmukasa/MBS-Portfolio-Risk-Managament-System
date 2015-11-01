import os
import django
from random import uniform, choice, randrange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from faker import Factory
from risk_management.models import AssumptionProfile, RiskProfile, RiskFactor, RiskConditional

fake = Factory.create()


def create_assumption_profiles():
    assumption_profile_names = [
        'GDP Growing at 3%', 'GDP Shrinking at 5%', 'Alien Invasion',
        'Minimum Wage Rate Hike', 'Donald Trump Presidency',
        'Bernie Sanders Presidency', 'Zombie Apocalypse'
    ]
    count = 0

    for name in assumption_profile_names:
        assumption_profile = AssumptionProfile()
        assumption_profile.name = name
        assumption_profile.gdp_growth = round(uniform(-6, 6), 4)
        assumption_profile.unemployment_rate = round(uniform(5, -15), 4)
        assumption_profile.national_home_price_index_growth = round(uniform(-20, 20), 4)
        assumption_profile.high_yield_spread = round(uniform(2, 20), 4)

        if count % 2 == 0:
            assumption_profile.constant_default_rate = round(uniform(0.5, 25), 4)
            assumption_profile.constant_prepayment_rate = round(uniform(5, 25), 4)
            assumption_profile.recovery = round(uniform(0, 100), 4)
        else:
            assumption_profile.constant_default_rate = -100
            assumption_profile.constant_prepayment_rate = -100
            assumption_profile.recovery = -100

        assumption_profile.lag = 128

        count += 1
        assumption_profile.save()


def create_risk_profiles():
    risk_profile_names = [
        'East Coast States', 'Midwest States', 'West Coast States', 'Popular States', 'Unpopular States',
        'Declining States', 'Emerging States', 'Growth States', 'Rural States', 'Urban States',
        'Pre-qualified FICO', 'Sub-prime FICO', 'Mid-range FICO', 'Less than 5 Years Remaining Term',
        'Less than 8 Years Remaining Term', 'Less than 10 Years Remaining Term',
        'Less than 15 Years Remaining Term', 'Less than 20 Years Remaining Term',
        'Current Interest Rate Above 2%', 'Current Interest Rate Above 5%', 'Current Interest Rate Above 8%'
    ]

    for name in risk_profile_names:
        risk_profile = RiskProfile()
        risk_profile.name = name
        risk_profile.save()


def create_risk_factors():
    risk_profiles = RiskProfile.objects.all()

    count = 0

    for profile in risk_profiles:
        risk_factor_number = randrange(3, 10)

        for i in range(risk_factor_number):
            pass


if __name__ == '__main__':
    print("Starting seed script...")
    create_assumption_profiles()
    create_risk_profiles()
    create_risk_factors()
    print("Seeding complete...")
