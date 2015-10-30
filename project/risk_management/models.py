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
        (TYPE, 'Property Type'),
        (PURPOSE, 'Purpose'),
        (MORTGAGE_TYPE, 'Mortgage Type'),
        (LIEN, 'Lien Position'),
        (CIR, 'Current Interest Rate'),
        (RT, 'Remaining Term'),
        (STATE, 'State'),
        (PMI, 'PMI'),  # TODO Figure out acronym
        (ZIP, 'Zipcode'),
        (FICO, 'FICO'),  # TODO Figure out acronym
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
        (GREATER_EQ, 'Greater Than of Equal To - >='),
        (LESSER_EQ, 'Lesser Than or Equal To - <='),
        (EQUAL, 'Equal To - ==')
    )
    risk_factor = models.ForeignKey(RiskFactor)
    conditional = models.CharField(max_length=64, choices=RISK_CONDITIONAL_CHOICES)
    value = models.CharField(max_length=64)


class AssumptionProfile(models.Model):
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    gdp = models.IntegerField()
    unemployment_rate = models.DecimalField(decimal_places=4, max_digits=10)
    national_home_price_index = models.DecimalField(decimal_places=4, max_digits=10)
    constant_default_rate = models.DecimalField(decimal_places=4, max_digits=10)
    constant_prepayment_rate = models.DecimalField(decimal_places=4, max_digits=10)
    recovery = models.DecimalField(decimal_places=4, max_digits=10)
    lag = models.DecimalField(decimal_places=4, max_digits=10)


class ScoreCard(models.Model):
    total_score = models.DecimalField(decimal_places=4, max_digits=10)
    updated_total_score = models.DecimalField(decimal_places=4, max_digits=10)


class ScoreCardProfile(models.Model):
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    cdr_score_card = models.ForeignKey(ScoreCard, related_name='+')
    cdp_score_card = models.ForeignKey(ScoreCard, related_name='+')
    recovery_score_card = models.ForeignKey(ScoreCard, related_name='+')
    lag_score_card = models.ForeignKey(ScoreCard, related_name='+')


class ScoreCardAttribute(models.Model):
    score_card = models.ForeignKey(ScoreCard)
    attribute = models.CharField(max_length=32)
    weight = models.DecimalField(decimal_places=4, max_digits=10)
    original_index = models.DecimalField(decimal_places=2, max_digits=5)
    original_score = models.DecimalField(decimal_places=4, max_digits=10)
    index_change = models.DecimalField(decimal_places=2, max_digits=5)
    updated_score = models.DecimalField(decimal_places=4, max_digits=10)


class Scenario(models.Model):
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    assumption_profile = models.ForeignKey(AssumptionProfile)
    score_card_profile = models.ForeignKey(ScoreCardProfile)
    risk_profiles = models.ManyToManyField(RiskProfile)
