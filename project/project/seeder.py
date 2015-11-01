import os
import django
from random import uniform

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from faker import Factory
from risk_management.models import AssumptionProfile

fake = Factory.create()


def create_assumption_profiles(profile_number=10):
    count = 0
    for assumption_profile in range(profile_number):
        assumption_profile = AssumptionProfile()
        assumption_profile.name = fake.company()
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


if __name__ == '__main__':
    print("Starting seed script...")
    create_assumption_profiles(6)
    print("Seeding complete...")
