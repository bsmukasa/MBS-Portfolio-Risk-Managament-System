from django.db import models


# Create your models here.
class RiskProfile(models.Model):
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class RiskFactor(models.Model):
    TYPE = 'property_type'
    PURPOSE = 'purpose'
    MORTGAGE_TYPE = 'mortgage_type'
    LIEN = 'lien_position'
    CIR = 'current_interest_rate'
    RT = 'remaining_term'
    STATE = 'state'
    PMI = 'PMI'  # TODO Figure out acronym
    ZIP = 'zipcode'
    FICO = 'FICO'  # TODO Figure out acronym
    MARGIN = 'gross_margin'
    ICAP = 'ICAP'  # TODO Figure out acronym
    LCAP = 'LCAP'  # TODO Figure out acronym
    INTEREST_ADJ_DATE = 'first_interest_adjustment_date'
    LTV = 'current_LTV'
    RISK_FACTOR_ATTRIBUTE_CHOICES = (
        (FICO, 'FICO'),  # TODO Figure out acronym
        (TYPE, 'Property Type'),
        (PURPOSE, 'Purpose'),
        (MORTGAGE_TYPE, 'Mortgage Type'),
        (LIEN, 'Lien Position'),
        (CIR, 'Current Interest Rate'),
        (RT, 'Remaining Term'),
        (STATE, 'State'),
        (PMI, 'PMI'),  # TODO Figure out acronym
        (ZIP, 'Zipcode'),
        (MARGIN, 'Gross Margin'),
        (ICAP, 'Interest Cap'),
        (LCAP, 'LCAP'),  # TODO Figure out acronym
        (INTEREST_ADJ_DATE, 'First Interest Adjustment Date'),
        (LTV, 'Current LTV')  # TODO Figure out acronym
    )

    CDR = 'cdr'
    CPR = 'cpr'
    RECOV = 'recovery'
    LAG = 'lag'
    CHANGING_ASSUMPTION_CHOICES = (
        ('CDR', 'Constant Default Rate'),
        ('CPR', 'Constant Prepayment Rate'),
        ('RECOV', 'Recovery'),
        ('LAG', 'Lag')
    )

    risk_profile = models.ForeignKey(RiskProfile)
    attribute = models.CharField(max_length=64, choices=RISK_FACTOR_ATTRIBUTE_CHOICES)
    changing_assumption = models.CharField(max_length=64, choices=CHANGING_ASSUMPTION_CHOICES)
    percentage_change = models.DecimalField(decimal_places=4, max_digits=20)


class RiskConditional(models.Model):
    GREATER = '>'
    LESSER = '<'
    GREATER_EQ = '>='
    LESSER_EQ = '<='
    EQUAL = '=='
    RISK_CONDITIONAL_CHOICES = (
        (GREATER, 'Greater Than - >'),
        (LESSER, 'Lesser Than - <'),
        (GREATER_EQ, 'Greater Than or Equal To - >='),
        (LESSER_EQ, 'Lesser Than or Equal To - <='),
        (EQUAL, 'Equal To - ==')
    )
    risk_factor = models.ForeignKey(RiskFactor)
    conditional = models.CharField(max_length=64, choices=RISK_CONDITIONAL_CHOICES)
    value = models.CharField(max_length=256)


class AssumptionProfile(models.Model):
    """

    Economic Assumptions and their typical ranges are:
        - gdp_growth                => -6% to +6%
        - unemployment_rate         =>  5% to 15%
        - national_home_price_index => -20% to +20%
        - high_yeild_spread         =>  2% to 20%

    Default Assumptions and their typical ranges are:
        - constant_default_rate     =>  0.5% to 25%
        - constant_prepayment_rate  =>  5% to 25%
        - recovery                  =>  0% to 100%
        - lag                       =>

    Economic Assumptions are used to calculate Default Assumptions. All Economic Assumptions
    are given equal weight and impact the Default Assumptions in the following ways:
            - Constant Default Rate (CDR):
                - GDP% , -6% = 25%, +6% = 0.5% CDR
                - Unemployment: 5% = 0.5% CDR, 15% = 25%
            - Constant Prepayment Rate (CPR):
                - High Yield Spread affects CPR: 2% spread = 25% prepayment , 20% = 0 prepayment.
                (At 20% it means our interest rates are insanely high) or maybe instead of 0, set the lower bound to  5%
            - Recoveries:
                - HPI (home price index) affects the recoveries. -20% = 0 recovery, 20% = 100% recovery
    """
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # Economic Assumptions
    gdp_growth = models.DecimalField(decimal_places=4, max_digits=10)
    unemployment_rate = models.DecimalField(decimal_places=4, max_digits=10)
    national_home_price_index_growth = models.DecimalField(decimal_places=4, max_digits=10)
    high_yield_spread = models.DecimalField(decimal_places=4, max_digits=10)

    # Default Assumptions
    constant_default_rate = models.DecimalField(decimal_places=4, max_digits=10)
    constant_prepayment_rate = models.DecimalField(decimal_places=4, max_digits=10)
    recovery = models.DecimalField(decimal_places=4, max_digits=10)
    lag = models.DecimalField(decimal_places=4, max_digits=10)


class ScoreCardProfile(models.Model):
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class ScoreCard(models.Model):
    ASSUMPTION_CHOICES = (
        ('CDR', 'Constant Default Rate'),
        ('CPR', 'Constant Prepayment Rate'),
        ('RECOV', 'Recovery'),
        ('LAG', 'Lag')
    )

    score_card_profile = models.ForeignKey(ScoreCardProfile)
    assumption_type = models.CharField(max_length=64, choices=ASSUMPTION_CHOICES)
    # total_score = models.DecimalField(decimal_places=4, max_digits=10)
    # updated_total_score = models.DecimalField(decimal_places=4, max_digits=10)


class ScoreCardAttribute(models.Model):
    score_card = models.ForeignKey(ScoreCard)
    attribute = models.CharField(max_length=32)
    weight = models.DecimalField(decimal_places=4, max_digits=10)
    original_index = models.DecimalField(decimal_places=2, max_digits=5)
    original_score = models.DecimalField(decimal_places=4, max_digits=10)
    # index_change = models.DecimalField(decimal_places=2, max_digits=5)
    # updated_score = models.DecimalField(decimal_places=4, max_digits=10)


# class Scenario(models.Model):
#     name = models.CharField(max_length=128)
#     date_created = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now=True)
#     assumption_profile = models.ForeignKey(AssumptionProfile)
#     score_card_profile = models.ForeignKey(ScoreCardProfile)
#     risk_profiles = models.ManyToManyField(RiskProfile)
