import os
import django
from random import uniform, choice, randrange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from faker import Factory
from risk_management.models import AssumptionProfile, RiskProfile, RiskFactor, RiskConditional, ScoreCardProfile, \
    ScoreCard, ScoreCardAttribute

fake = Factory.create()


def create_assumption_profiles():
    """ Create assumption profiles and save them to the database.


    """
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
    """ Create risk profiles and save them to the database.


    """
    risk_profile_names = [
        'East Coast States', 'Midwest States', 'West Coast States', 'Popular States', 'Unpopular States',
        'Declining States', 'Emerging States', 'Growth States', 'Rural States', 'Urban States',
        'Pre-qualified FICO', 'Sub-prime FICO', 'Mid-range FICO', 'Less than 5 Years Remaining Term',
        'Prime Remaining Term', 'Less than 10 Years Remaining Term',
        'Less Optimal Remaining Term', 'Less than 20 Years Remaining Term',
        'Current Interest Rate Above 2%', 'Current Interest Rate Above 5%', 'Current Interest Rate Above 8%'
    ]

    risk_profiles = []
    for name in risk_profile_names:
        risk_profiles.append(RiskProfile(name=name))

    RiskProfile.objects.bulk_create(risk_profiles)


def create_risk_factors():
    risk_profiles = RiskProfile.objects.all()

    risk_factors = []
    for count, profile in enumerate(risk_profiles):
        if count < 10:
            attribute = 'state'
        elif count < 13:
            attribute = 'FICO'
        elif count < 18:
            attribute = 'remaining_term'
        else:
            attribute = 'current_interest_rate'

        assumptions_list = ['CDR', 'CPR', 'RECOV', 'LAG']

        risk_factor_number = randrange(3, 10)
        for i in range(risk_factor_number):
            risk_factor = RiskFactor(
                risk_profile=profile,
                attribute=attribute,
                changing_assumption=choice(assumptions_list),
                percentage_change=round(uniform(-10, 10), 4)
            )

            risk_factors.append(risk_factor)

    RiskFactor.objects.bulk_create(risk_factors)


def create_risk_conditionals():
    risk_factors = RiskFactor.objects.all()

    risk_conditionals = []
    for factor in risk_factors:
        conditional = None
        if factor.attribute == 'state':
            state = fake.state_abbr()
            conditional = RiskConditional(
                risk_factor=factor,
                conditional='==',
                value=state
            )
        elif factor.attribute == 'FICO':
            conditional = RiskConditional(
                risk_factor=factor,
                conditional='>',
                value=randrange(300, 450)
            )
            risk_conditionals.append(conditional)

            conditional = RiskConditional(
                risk_factor=factor,
                conditional='<',
                value=randrange(500, 850)
            )
        elif factor.attribute == 'remaining_term':
            term_list = [5, 8, 10, 15, 20, 25, 30]
            conditional = RiskConditional(
                risk_factor=factor,
                conditional='<',
                value=choice(term_list)
            )
        elif factor.attribute == 'current_interest_rate':
            interest_list = [2, 5, 7, 8, 9, 11]
            conditional = RiskConditional(
                risk_factor=factor,
                conditional='>',
                value=choice(interest_list)
            )

        risk_conditionals.append(conditional)

    RiskConditional.objects.bulk_create(risk_conditionals)


def create_score_card_profiles():
    card_profile_name_list = ['Default', 'Nintendo', 'Sony', 'Microsoft']
    score_card_profiles = []
    for name in card_profile_name_list:
        profile = ScoreCardProfile(name=name)
        score_card_profiles.append(profile)

    ScoreCardProfile.objects.bulk_create(score_card_profiles)


def add_assumption_score_cards():
    score_card_profiles = ScoreCardProfile.objects.all()

    score_cards = []
    for profile in score_card_profiles:
        score_cards.append(ScoreCard(
            score_card_profile=profile,
            assumption_type='CDR',
        ))
        score_cards.append(ScoreCard(
            score_card_profile=profile,
            assumption_type='CPR',
        ))
        score_cards.append(ScoreCard(
            score_card_profile=profile,
            assumption_type='RECOV',
        ))
        score_cards.append(ScoreCard(
            score_card_profile=profile,
            assumption_type='LAG',
        ))

    ScoreCard.objects.bulk_create(score_cards)


def add_score_card_attributes():
    attribute_list = [
        'property_type', 'purpose', 'mortgage_type', 'lien_position',
        'current_interest_rate', 'remaining_term', 'state', 'PMI',
        'zipcode', 'FICO', 'gross_margin', 'ICAP', 'LCAP',
        'first_interest_adjustment_date', 'current_LTV'
    ]
    score_cards = ScoreCard.objects.all()

    score_card_attributes = []

    for card in score_cards:
        for attribute in attribute_list:
            weight = 100 / len(attribute_list)
            original_score = weight

            score_card_attributes.append(ScoreCardAttribute(
                score_card=card,
                attribute=attribute,
                weight=weight,
                original_index=1,
                original_score=original_score
            ))

    ScoreCardAttribute.objects.bulk_create(score_card_attributes)

if __name__ == '__main__':
    print("Starting seed script...")
    create_assumption_profiles()
    print("Assumptions created...")
    create_risk_profiles()
    print("Risk profiles created...")
    create_risk_factors()
    print("Risk factors created...")
    create_risk_conditionals()
    print("Risk conditionals created...")
    create_score_card_profiles()
    print("Score card profiles created...")
    add_assumption_score_cards()
    print("Assumption score cards added...")
    add_score_card_attributes()
    print("Score attributes added...")
    print("Seeding complete...")
