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
        'Prime Remaining Term', 'Less than 10 Years Remaining Term',
        'Less Optimal Remaining Term', 'Less than 20 Years Remaining Term',
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
            if count < 10:
                create_state_risk_factor(profile)
            elif count < 13:
                create_fico_risk_factor(profile)
            elif count < 18:
                create_remaining_term_factor(profile, count)
        count += 1


def create_state_risk_factor(risk_profile):
    assumptions_list = ['CDR', 'CPR', 'RECOV', 'LAG']
    risk_factor = RiskFactor(
        risk_profile=risk_profile,
        attribute='state',
        changing_assumption=choice(assumptions_list),
        percentage_change=round(uniform(-10, 10), 4)
    )
    risk_factor.save()
    risk_conditional = RiskConditional()
    risk_conditional.risk_factor = risk_factor
    risk_conditional.conditional = '=='
    risk_conditional.value = fake.state_abbr()
    risk_conditional.save()

    return risk_factor


def create_fico_risk_factor(risk_profile):
    assumptions_list = ['CDR', 'CPR', 'RECOV', 'LAG']
    risk_factor = RiskFactor(
        risk_profile=risk_profile,
        attribute='FICO',
        changing_assumption=choice(assumptions_list),
        percentage_change=round(uniform(-10, 10), 4)
    )
    risk_factor.save()
    risk_conditional1 = RiskConditional()
    risk_conditional1.risk_factor = risk_factor
    risk_conditional1.conditional = '>'
    risk_conditional1.value = randrange(300, 450)
    risk_conditional1.save()
    risk_conditional2 = RiskConditional()
    risk_conditional2.risk_factor = risk_factor
    risk_conditional2.conditional = '<'
    risk_conditional2.value = randrange(500, 850)
    risk_conditional2.save()


def create_remaining_term_factor(risk_profile, count):
    assumptions_list = ['CDR', 'CPR', 'RECOV', 'LAG']
    risk_factor = RiskFactor(
        risk_profile=risk_profile,
        attribute='remaining_term',
        changing_assumption=choice(assumptions_list),
        percentage_change=round(uniform(-10, 10), 4)
    )
    risk_factor.save()

    risk_conditional = RiskConditional()
    risk_conditional.risk_factor = risk_factor
    risk_conditional.conditional = '<'

    if count == 13:
        risk_conditional.value = 5
    elif count == 14:
        risk_conditional.value = 8
    elif count == 15:
        risk_conditional.value = 10
    elif count == 16:
        risk_conditional.value = 15
    elif count == 17:
        risk_conditional.value = 20

    risk_conditional.save()


if __name__ == '__main__':
    print("Starting seed script...")
    create_assumption_profiles()
    create_risk_profiles()
    create_risk_factors()
    print("Seeding complete...")
