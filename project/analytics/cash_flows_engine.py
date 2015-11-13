from itertools import chain

import numpy as np
import pandas as pd


class LoanPortfolio:
    def __init__(self, discount_rate, loan_df, cash_flow_df=None):
        self.discount_rate = discount_rate
        self.loan_df = loan_df[[
            'current_principal_balance', 'current_interest_rate', 'remaining_term',
            'adjusted_cdr', 'adjusted_cpr', 'adjusted_recovery'
        ]]

        if cash_flow_df is None:
            self.cash_flows_df = self.cash_flows_data_frame_for_portfolio()
            self.cash_flows_df['losses'] = self.losses_for_cash_flow()
            self.cash_flows_df['total_interest'] = self.total_interests_for_cash_flow()
            self.cash_flows_df['total_principal'] = self.total_principals_for_cash_flow()
            self.cash_flows_df['total_payments'] = self.total_payments_for_cash_flow()
        else:
            self.cash_flows_df = cash_flow_df

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
            original_balance=float(row['current_principal_balance']),
            interest_rate=float(row['current_interest_rate']),
            maturity=row['remaining_term'],
            cdr=row['adjusted_cdr'],
            cpr=row['adjusted_cpr'],
            recovery_percentage=row['adjusted_recovery']
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

    def interest_aggregate_for_portfolio(self):
        """ Gets the portfolio's total interest from aggregate cash flows.

        Returns: Portfolio's aggregate total interest from cash flows.

        """
        return self.cash_flows_df['total_interest'].sum()

    def scheduled_principal_aggregate_for_portfolio(self):
        """ Gets the portfolio's total scheduled principal from aggregate cash flows.

        Returns: Portfolio's aggregate total scheduled principal from cash flows.

        """
        return self.cash_flows_df['scheduled_principal'].sum()

    def unscheduled_principal_aggregate_for_portfolio(self):
        """ Gets the portfolio's total unscheduled principal from aggregate cash flows.

        Returns: Portfolio's aggregate total unscheduled principal from cash flows.

        """
        return self.cash_flows_df['unscheduled_principal'].sum()

    def defaults__aggregate_for_portfolio(self):
        """ Gets the portfolio's total defaults from aggregate cash flows.

        Returns: Portfolio's aggregate total defaults from cash flows.

        """
        return self.cash_flows_df['defaults'].sum()

    def losses_aggregate_for_portfolio(self):
        """ Gets the portfolio's total losses from aggregate cash flows.

        Returns: Portfolio's aggregate total losses from cash flows.

        """
        return self.cash_flows_df['losses'].sum()

    def recovery_aggregate_for_portfolio(self):
        """ Gets the portfolio's total recovery value from aggregate cash flows.

        Returns: Portfolio's aggregate total recoveries from cash flows.

        """
        return self.cash_flows_df['recovery'].sum()

    def cash_flows_aggregate_for_portfolio(
            self,
            fields_list=(
                'start_balance',
                'scheduled_principal',
                'unscheduled_principal',
                'interest', 'defaults',
                'losses',
                'recovery'
            )
    ):
        """ Generates a portfolio's aggregate cash flows for a given set of fields.

        Args:
            fields_list: The list of fields from a loan cash flows to be aggregated.

        Returns: The portfolio's aggregated cash flows.

        """
        aggregate_cash_flows_df = self.cash_flows_df.groupby('period')[
            fields_list
        ].sum().reset_index()
        return aggregate_cash_flows_df

    def net_present_values_for_portfolio(self):
        """ Calculates net present values for each loan in a portfolio.

        Returns: A series representing the net present values of each loan.

        """
        npv_series = self.loan_df.apply(
            self.net_present_value_for_loan,
            axis=1
        )
        return npv_series

    def net_present_value_for_loan(self, loan):
        """ Calculates a loan's net present value from its cash flows.

        Args:
            loan: The loan which is being valued.

        Returns: The net present value of the loan.

        """
        cash_flows = self.cash_flows_df[self.cash_flows_df['loan_df_pk'] == loan.name]
        npv = np.npv(self.discount_rate / 12, cash_flows['total_payment'])
        return npv

    def net_present_value_aggregate_for_portfolio(self):
        """ Gets the portfolio's aggregate net present value.

        Returns: The portfolio's aggregate net present value.

        """
        df = self.cash_flows_df.groupby('period')['total_payment'].sum().reset_index()
        npv = np.npv(self.discount_rate / 12, df['total_payment'])
        return npv

    def internal_rates_of_return_for_portfolio(self):
        """ Calculates the internal rates of return for each loan in a portfolio.

        Returns: A series representing the internal rates of return of each loan.

        """
        internal_rate_of_return_series = self.loan_df.apply(
            self.internal_rate_of_return_for_loan,
            axis=1
        )
        return internal_rate_of_return_series

    def internal_rate_of_return_for_loan(self, loan):
        """ Calculates a loan's internal rate of return from its cash flows.

        Args:
            loan: The loan which is being considered.

        Returns: The internal rate of return of the loan.

        """
        cash_flows = self.cash_flows_df[self.cash_flows_df['loan_df_pk'] == loan.name]
        total_payments = list(cash_flows['total_payment'])
        total_payments[0] = -loan['Original_Amount']
        internal_rate_of_return = np.irr(total_payments)
        return internal_rate_of_return

    # TODO Portfolio IRR MUST BE FROM AGG CASH FLOWS - NOT SUM
    def internal_rate_of_return_aggregate_for_portfolio(self):
        """ Calculates the portfolio's aggregate internal rate of return.

        Returns: The portfolio's aggregate internal rate of return.

        """
        return self.internal_rates_of_return_for_portfolio().sum()


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
