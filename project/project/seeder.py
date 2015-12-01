import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from risk_management.models import AssumptionProfile, RiskProfile, RiskFactor


def create_assumption_profiles():
    with open('assumptions_profiles.csv') as csv_file:
        assumption_profiles = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            assumption_profiles.append(AssumptionProfile(
                name=row['name'],
                gdp_growth=row['gdp_growth'],
                unemployment_rate=row['unemployment_rate'],
                national_home_price_index_growth=row['national_home_price_index_growth'],
                high_yield_spread=row['high_yield_spread'],
                constant_default_rate=row['constant_default_rate'],
                constant_prepayment_rate=row['constant_prepayment_rate'],
                recovery_percentage=row['recovery_percentage']
            ))
        AssumptionProfile.objects.bulk_create(assumption_profiles)


def create_risk_profiles():
    with open('risk_profiles.csv') as csv_file:
        risk_profiles = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            risk_profiles.append(RiskProfile(name=row['name']))
        RiskProfile.objects.bulk_create(risk_profiles)


def create_risk_factors():
    with open('risk_factors.csv') as csv_file:
        risk_factors = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            risk_factors.append(RiskFactor(
                risk_profile_id=row['risk_profile_id'],
                attribute=row['attribute'],
                changing_assumption=row['changing_assumption'],
                percentage_change=row['percentage_change']
            ))
        RiskFactor.objects.bulk_create(risk_factors)


if __name__ == '__main__':
    print("Starting seed script...")
    create_assumption_profiles()
    print("Assumptions created...")
    create_risk_profiles()
    print("Risk profiles created...")
    create_risk_factors()
    print("Risk factors created...")
    print("Seeding complete...")
