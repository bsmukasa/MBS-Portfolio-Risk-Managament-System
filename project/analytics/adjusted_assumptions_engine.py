from portfolio.models import Loan
from risk_management.models import Scenario


def get_adjusted_assumptions(scenario_id, portfolio_id):
    scenario = Scenario.objects.get(scenario_id=scenario_id)
    assumptions = scenario.assumption_profile
    risk_list = scenario.risk_profiles.all()

