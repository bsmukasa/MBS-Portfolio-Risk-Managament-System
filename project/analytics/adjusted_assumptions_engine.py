from portfolio.models import Loan
from risk_management.models import Scenario


def get_adjusted_assumptions(scenario_id, portfolio_id):
    scenario = Scenario.objects.get(scenario_id=scenario_id)
    assumptions = scenario.assumption_profile
    risks = scenario.risk_profiles

    loans = Loan.objects.get(portfolio_id=portfolio_id)
