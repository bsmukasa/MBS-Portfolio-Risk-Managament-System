import random
import pandas as pd
from portfolio.models import Loan
from risk_management.models import Scenario


def generate_adjusted_assumptions(portfolio_id, scenario_id):
    scenario = Scenario.objects.get(pk=scenario_id)

    assumptions = scenario.assumption_profile

    loan_df = pd.DataFrame(list(Loan.objects.filter(portfolio_id=portfolio_id).values()))

    # Add default economic assumptions.
    loan_df['constant_default_rate'] = float(assumptions.constant_default_rate) / 100
    loan_df['constant_prepayment_rate'] = float(assumptions.constant_prepayment_rate) / 100
    loan_df['recovery_percentage'] = float(assumptions.recovery_percentage) / 100

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
    return loan_df


def generate_adjusted_cdr(row):
    change = random_change()
    adjusted_cdr = row['constant_default_rate'] * change / 100

    if adjusted_cdr < 0.005:
        return 0.005
    elif adjusted_cdr > 0.25:
        return 0.25
    return adjusted_cdr


def generate_adjusted_cpr(row):
    adjusted_cpr = row['constant_prepayment_rate'] * random_change(factor_number=5) / 100
    if adjusted_cpr > 0.25:
        return 0.25
    elif adjusted_cpr < 0.05:
        return 0.05
    return adjusted_cpr


def generate_adjusted_recovery(row):
    recovery = row['recovery_percentage'] * random_change(factor_number=1) / 100
    if recovery < 0:
        return 0.0
    elif recovery > 1.0:
        return 1.0
    return recovery


def random_change(factor_number=3, change_range=5, how_many_chances=5):
    change = 0
    for i in range(factor_number):
        chance = random.randrange(how_many_chances)
        if chance == 1:
            change += random.uniform(-change_range, change_range)
    return 100 + change


def pandas_data_frame_columns_to_float(data_frame, field_list):
    print('CASTING TYPES STARTED')
    print('Field List: ', field_list)
    data_frame[field_list] = data_frame[field_list].astype(float)
    print(data_frame.dtypes)
    return data_frame
