from itertools import chain
import pandas as pd


class LoanPortfolio:
    def __init__(self, csv_file):
        """ Creates an instance of LoanPortfolio for use in cash flows generation.

        :param csv_file: The csv file containing the loans.
        """
        self.csv_file = csv_file
        self.loan_df = pd.read_csv(csv_file)

        self.cash_flows_df = self.create_cash_flows_data_frame()
        self.cash_flows_df['losses'] = self.calculate_cash_flow_losses()
        self.cash_flows_df['total_interest'] = self.calculate_cash_flow_total_interests()
        self.cash_flows_df['total_principal'] = self.calculate_cash_flow_total_principals()
        self.cash_flows_df['total_payments'] = self.calculate_cash_flow_total_payments()

    def create_cash_flows_data_frame(self):
        """ Creates a pandas DataFrame containing all of cash flows for the loans in the LoanPortfolio.

        :return: Cash flows data frame.
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

        :param row: The panda DataFrame row representation of a loan.
        :return: Cash flows represented as a list of period dictionaries.
        """
        cash_flows_list_of_dicts = create_payment_schedule(
            loan_df_pk=row.name,
            original_balance=row['Original_Amount'],
            interest_rate=row['Current_Interest_Rate'],
            maturity=row['Original_Term'],
            cdr=row['Current_Default_Rate'],
            cpr=row['Current_Prepayment_Rate'],
            recov=row['Recovery']
        )
        return cash_flows_list_of_dicts

    def calculate_cash_flow_losses(self):
        """ Calculates the losses for all periods in a cash flows pandas DataFrame.

        :return: A pandas Series of period losses.
        """
        return self.cash_flows_df['defaults'] - self.cash_flows_df['recovery']

    def calculate_cash_flow_total_interests(self):
        """ Calculates the total interest for all periods in a cash flows pandas DataFrame.

        :return: A pandas Series of period total interests.
        """
        return self.cash_flows_df['interest']

    def calculate_cash_flow_total_principals(self):
        """ Calculates the total principal for all periods in a cash flows pandas DataFrame.

        :return: A pandas Series of period total principals.
        """
        total_principals = self.cash_flows_df['scheduled_principal'] + self.cash_flows_df['unscheduled_principal']
        total_principals += self.cash_flows_df['recovery']
        return total_principals

    def calculate_cash_flow_total_payments(self):
        """ Calculates the total payments for all periods in a cash flows pandas DataFrame.

        :return: A pandas Series of period total payments.
        """
        return self.cash_flows_df['total_interest'] + self.cash_flows_df['total_principal']


def create_payment_schedule(loan_df_pk, original_balance, interest_rate, maturity, cdr, cpr, recov):
    """ Creates a payment schedule or cash flows for a loan.

    Payment schedules are presented as a list of "period" dictionaries. Each period representing one period
    of the maturity or term. A O period is created to represent the outflow of acquiring the loan. All
    subsequent periods represent incoming cash flows.

    :param loan_df_pk: The loan primary key.
    :param original_balance: The original balance of the loan.
    :param interest_rate: The yearly interest rate of the loan.
    :param maturity: The maturity or term of the loan.
    :param cdr: The constant default rate of the loan.
    :param cpr: The constant prepayment rate of the loan.
    :param recov: The recovery percentage of the loan.
    :return: A payment schedule represented as a list of period dictionaries.

    :Example:
    >>> schedule = create_payment_schedule(1, 100000, 0.04, 120, 0.09, 0.02, 0.95)
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
        interest=0,
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
            cdr, cpr, i, interest_rate, recov
        )
        period_list[i] = period

    return period_list


def create_payment_schedule_period(
        loan_df_pk, start_balance, remaining_term,
        cdr, cpr, period_num, interest_rate, recov
):
    """ Create a period and associated information for a loan's payment schedule or cash flows.

    :param loan_df_pk: The loan primary key.
    :param start_balance: The balance at the beginning of the period.
    :param remaining_term: The remaining terms after this period.
    :param cdr: The constant default rate.
    :param cpr: The constant prepayment rate.
    :param period_num: The period number.
    :param interest_rate: The yearly interest rate.
    :param recov: The recovery percentage.
    :return: A period represented as a dictionary.

    :Example:
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
    recovery = recov * defaults

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

    :param start_balance: The starting balance of the loan.
    :param monthly_interest_rate: The monthly interest rate of the loan.
    :param term: The term of the loan.
    :return: The monthly payment.

    :Example:
    >>> pymt = calculate_monthly_payment(100000, 0.003333333, 120)
    >>> print(pymt)
    1012.451382
    """
    numerator = (start_balance * (monthly_interest_rate * ((1 + monthly_interest_rate) ** term)))
    denominator = ((1 + monthly_interest_rate) ** term - 1)
    payment = numerator / denominator * 1.0
    return payment

if __name__ == '__main__':
    portfolio = LoanPortfolio('1000_loans_sample.csv')
    print(portfolio.cash_flows_df)
