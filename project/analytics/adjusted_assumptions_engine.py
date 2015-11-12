import pandas as pd

from portfolio.models import Loan
from risk_management.models import Scenario, RiskFactor


class ScoreCard:
    def __init__(self, assumption_type):
        self.assumption_type = assumption_type
        self.attributes = dict()
        for choice in RiskFactor.RISK_FACTOR_ATTRIBUTE_CHOICES:
            weight = 100 / len(RiskFactor.RISK_FACTOR_ATTRIBUTE_CHOICES)
            self.attributes[choice] = dict(weight=weight, index=1.0, original_score=weight)


def get_adjusted_assumptions(scenario_id, portfolio_id):
    score_card_types = ['CDR', 'CPR', 'RECOVERY']
    scenario = Scenario.objects.get(scenario_id=scenario_id)
    assumptions = scenario.assumption_profile
    risk_list = scenario.risk_profiles.all()

    attributes = dict()
    for choice in RiskFactor.RISK_FACTOR_ATTRIBUTE_CHOICES:
            weight = 100 / len(RiskFactor.RISK_FACTOR_ATTRIBUTE_CHOICES)
            attributes[choice] = dict(weight=weight, index=1.0, original_score=weight)

    cdr_df = pd

    loan_df = pd.DataFrame(list(Loan.objects.filter(portfolio_id=portfolio_id)))

