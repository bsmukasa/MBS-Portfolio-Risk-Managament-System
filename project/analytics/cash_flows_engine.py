from itertools import chain

import numpy as np
import pandas as pd


class LoanPortfolio:
    def __init__(self, portfolio_dict_list, discount_rate):
        """ Creates an instance of LoanPortfolio for use in cash flows generation.

        Args:
            portfolio_dict_list: The list of dictionaries representing the portfolios loans.
        """
        self.loan_df = pd.DataFrame(portfolio_dict_list)
        self.discount_rate = discount_rate

        self.cash_flows_df = self.cash_flows_data_frame_for_portfolio()
        self.cash_flows_df['losses'] = self.losses_for_cash_flow()
        self.cash_flows_df['total_interest'] = self.total_interests_for_cash_flow()
        self.cash_flows_df['total_principal'] = self.total_principals_for_cash_flow()
        self.cash_flows_df['total_payments'] = self.total_payments_for_cash_flow()

    def cash_flows_data_frame_for_portfolio(self):
        """ Creates a pandas DataFrame containing all of cash flows for the loans in the LoanPortfolio.

        Returns: Cash flows data frame.
        """
        cash_flow_list_list_dicts = self.loan_df.apply(
            self.generate_loan_cash_flows,
            axis=1
        )
        cash_flows_list_dicts = list(chain.from_iterable(cash_flow_list_list_dicts))
        cash_flows_data_frame = pd.DataFrame(cash_flows_list_dicts)
        return cash_flows_data_frame

    @staticmethod
    def generate_loan_cash_flows(row):
        """ Creates the cash flows for an individual loan.

        Args:
            row: The panda DataFrame row representation of a loan.

        Returns: Cash flows represented as a list of period dictionaries.
        """
        cash_flows_list_of_dicts = payment_schedule_for_loan(
            loan_df_pk=row.name,
            original_balance=row['Current_Principal_Balance'],
            interest_rate=row['Current_Interest_Rate'],
            maturity=row['Remaining_Term'],
            cdr=row['Current_Default_Rate'],
            cpr=row['Current_Prepayment_Rate'],
            recovery_percentage=row['Recovery']
        )
        return cash_flows_list_of_dicts

    def losses_for_cash_flow(self):
        """ Calculates the losses for all periods in a cash flows pandas DataFrame.

        Returns: A pandas Series of period losses.
        """
        return self.cash_flows_df['defaults'] - self.cash_flows_df['recovery']

    def total_interests_for_cash_flow(self):
        """ Calculates the total interest for all periods in a cash flows pandas DataFrame.

        :return: A pandas Series of period total interests.
        """
        return self.cash_flows_df['interest']

    def total_principals_for_cash_flow(self):
        """ Calculates the total principal for all periods in a cash flows pandas DataFrame.

        Returns: A pandas Series of period total principals.
        """
        total_principals = self.cash_flows_df['scheduled_principal'] + self.cash_flows_df['unscheduled_principal']
        total_principals += self.cash_flows_df['recovery']
        return total_principals

    def total_payments_for_cash_flow(self):
        """ Calculates the total payments for all periods in a cash flows pandas DataFrame.

        Returns: A pandas Series of period total payments.
        """
        return self.cash_flows_df['total_interest'] + self.cash_flows_df['total_principal']

    def current_balance_aggregate_for_portfolio(self):
        """ Gets the portfolio's total current balance.

        Returns: Portfolio's total current balance.

        """
        return self.loan_df['Current_Principal_Balance'].sum()


def payment_schedule_for_loan(loan_df_pk, original_balance, interest_rate, maturity, cdr, cpr, recovery_percentage):
    """ Creates a payment schedule or cash flows for a loan.

    Payment schedules are presented as a list of "period" dictionaries. Each period representing one period
    of the maturity or term. A O period is created to represent the outflow of acquiring the loan. All
    subsequent periods represent incoming cash flows.

    Args:
        loan_df_pk: The loan primary key.
        original_balance: The original balance of the loan.
        interest_rate: The yearly interest rate of the loan.
        maturity: The maturity or term of the loan.
        cdr: The constant default rate of the loan.
        cpr: The constant prepayment rate of the loan.
        recovery_percentage: The recovery percentage of the loan.
        
    Returns: A payment schedule represented as a list of period dictionaries.

    Examples:
    >>> schedule = payment_schedule_for_loan(1, 100000, 0.04, 120, 0.09, 0.02, 0.95)
    >>> print(schedule)
    [
        {
            loan_df_pk: 1, period: 0, start_balance: 0.000000, remaining_term: 121,
            interest: 0.000000, payment: 0.000000, scheduled_principal: 0.000000,
            unscheduled_principal: 0, defaults: 0.000000, recovery: 0.000000,
            end_balance: 100000.000000
        },
        {
            loan_df_pk: 1, period: 1, start_balance: 100000.000000, remaining_term: 120,
            interest: 333.333333, payment: 1012.451382, scheduled_principal: 679.118048,
            unscheduled_principal: 0, defaults: 750.000000, recovery: 712.500000,
            end_balance: 98404.215285
        },
        .....etc....
    ]
    """
    period_0 = dict(
        loan_df_pk=loan_df_pk,
        period=0,
        start_balance=0,
        remaining_term=maturity + 1,
        interest=-original_balance,
        payment=0,
        scheduled_principal=0,
        unscheduled_principal=0,
        defaults=0,
        recovery=0,
        end_balance=original_balance
    )
    period_list = [0] * (maturity + 1)
    period_list[0] = period_0

    for i in range(1, maturity + 1):
        last_period = period_list[i - 1]

        period = create_payment_schedule_period(
            loan_df_pk, last_period['end_balance'], last_period['remaining_term'] - 1,
            cdr, cpr, i, interest_rate, recovery_percentage
        )
        period_list[i] = period

    return period_list


def create_payment_schedule_period(
        loan_df_pk, start_balance, remaining_term,
        cdr, cpr, period_num, interest_rate, recovery_percentage
):
    """ Create a period and associated information for a loan's payment schedule or cash flows.

    Args:
        loan_df_pk: The loan primary key.
        start_balance: The balance at the beginning of the period.
        remaining_term: The remaining terms after this period.
        cdr: The constant default rate.
        cpr: The constant prepayment rate.
        period_num: The period number.
        interest_rate: The yearly interest rate.
        recovery_percentage: The recovery percentage.
    
    Returns: A period represented as a dictionary.

    Examples:
    >>> period = create_payment_schedule_period(5, 87745.253381, 112, 0.09, 0.02, 9, 0.04, 0.95)
    >>> print(period)
    {
        loan_df_pk: 5, period: 9, start_balance: 87745.253381, remaining_term: 118,
        interest: 292.484178, payment: 940.050272, scheduled_principal: 647.566094,
        unscheduled_principal: 993.848452, defaults: 658.089400, recovery: 625.184930,
        end_balance: 86293.355798
    }
    """
    interest = interest_rate / 12 * start_balance
    payment = calculate_monthly_payment(start_balance, interest_rate / 12, remaining_term)
    scheduled_principal = payment - interest
    unscheduled_principal = start_balance * cpr / 12
    defaults = start_balance * cdr / 12
    end_balance = start_balance - scheduled_principal - unscheduled_principal - defaults
    recovery = recovery_percentage * defaults

    period = dict(
        loan_df_pk=loan_df_pk,
        period=period_num,
        start_balance=start_balance,
        remaining_term=remaining_term,
        interest=interest,
        payment=payment,
        scheduled_principal=scheduled_principal,
        unscheduled_principal=unscheduled_principal,
        defaults=defaults,
        end_balance=end_balance,
        recovery=recovery
    )

    return period


def calculate_monthly_payment(start_balance, monthly_interest_rate, term):
    """ Calculates the fixed monthly payment of a loan given a term and without a future value.

    Args:
        start_balance: The starting balance of the loan.
        monthly_interest_rate: The monthly interest rate of the loan.
        term: The term of the loan.

    Returns: The monthly payment.

    Examples:
    >>> pymt = calculate_monthly_payment(100000, 0.003333333, 120)
    >>> print(pymt)
    1012.451382
    """
    numerator = (start_balance * (monthly_interest_rate * ((1 + monthly_interest_rate) ** term)))
    denominator = ((1 + monthly_interest_rate) ** term - 1)
    payment = numerator / denominator * 1.0
    return payment


def isfloat(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True


def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b
