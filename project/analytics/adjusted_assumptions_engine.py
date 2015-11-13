import random

import pandas as pd

from portfolio.models import Loan
from risk_management.models import Scenario


def get_adjusted_assumptions(scenario_id, portfolio_id):
    scenario = Scenario.objects.get(scenario_id=scenario_id)
    assumptions = scenario.assumption_profile

    loan_df = pd.DataFrame(list(Loan.objects.filter(portfolio_id=portfolio_id)))
    loan_df['constant_default_rate'] = assumptions.constant_default_rate
    loan_df['constant_repayment_rate'] = assumptions.constant_prepayment_rate
    loan_df['recovery'] = assumptions.recovery_percentage

    adjusted_cdr_series = loan_df.apply(
            generate_adjusted_cdr,
            axis=1
    )

    loan_df['adjusted_cdr'] = adjusted_cdr_series

    adjusted_cpr_series = loan_df.apply(
            generate_adjusted_cpr,
            axis=1
    )

    loan_df['adjusted_cpr'] = adjusted_cpr_series

    adjusted_recovery_series = loan_df.apply(
            generate_adjusted_recovery,
            axis=1
    )

    loan_df['adjusted_recovery'] = adjusted_recovery_series


def generate_adjusted_cdr(row):
    adjusted_cdr = row['Current_Default_Rate'] * random_change() / 100
    return adjusted_cdr


def generate_adjusted_cpr(row):
    adjusted_cpr = row['Current_Prepayment_Rate'] * random_change() / 100
    return adjusted_cpr


def generate_adjusted_recovery(row):
    recovery = row['Recovery'] * random_change() / 100
    return recovery


def random_change(factor_number=3, change_range=10, how_many_chances=5):
    change = 0
    for i in range(0, factor_number):
        chance = random.randrange(how_many_chances)
        if chance == 1:
            change += random.uniform(-change_range, change_range)
    return 100 + change
