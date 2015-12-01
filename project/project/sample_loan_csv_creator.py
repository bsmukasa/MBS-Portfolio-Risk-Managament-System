import csv
import random

import numpy as np
from faker import Factory
from barnum import gen_data
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import Loan

fake = Factory.create()


def create_loan(loan_id):
    address = gen_data.create_city_state_zip()
    property_type_code = get_property_type_code()
    original_appraisal_amount = random.randrange(68000, 620000, 1000)
    original_amount = random.randrange(0.75 * original_appraisal_amount, 0.98 * original_appraisal_amount, 1000)
    original_term = random.randrange(180, 360, 60)
    remaining_term = random.randint(0.6 * original_term, original_term)
    amortized_term = original_term
    fico = random.randint(480, 800)
    current_fico = fico + random.randint(-50, 50)
    # TODO Create function that generates accurate current interest rate from fico and ltv.
    current_interest_rate = random.uniform(0.03827, 0.11416)
    current_principal_balance = get_current_principal_balance(
        original_amount, current_interest_rate, original_term, remaining_term
    )
    return dict(
        LoanID=loan_id,
        Property=property_type_code,
        Occupancy='AB',
        CITY=address[1],
        STATE=address[2],
        ZIP=address[0],
        # as_of_date=,
        # first_payment_date=,
        # original_date=,
        # first_index_rate_adjustment_date=,
        FICO=fico,
        Current_FICO_Score=current_fico,
        Current_Interest_Rate=current_interest_rate,
        Original_Amount=original_amount,
        Original_Term=original_term,
        Original_Appraisal_Amount=original_appraisal_amount,
        Remaining_Term=remaining_term,
        Amor_Term=amortized_term,
        Current_Principal_Balance=current_principal_balance,
    )


def get_current_principal_balance(original_amount, annual_interest_rate, original_term, remaining_term):
    # noinspection PyTypeChecker
    monthly_payment = -np.pmt(annual_interest_rate / 12, original_term, original_amount)
    first_part = 12 * monthly_payment / annual_interest_rate
    second_part = first_part - original_amount
    third_part = (1 + annual_interest_rate / 12)**(original_term - remaining_term)
    return first_part - second_part * third_part


def get_property_type_code():
    return random.choice(Loan.PROPERTY_TYPE_CODE_CHOICES[0])


def next_bank_loan_id(last_id=None):
    return last_id + random.randint(151, 1127)


def generate_loan_csv_files(loan_number_list):
    bank_loan_id = random.randint(500000, 600000)
    for loan_number in loan_number_list:
        file_name = str(loan_number)
        file_name += '_sample_loans.csv'
        # TODO Update so that all field names are included.
        with open(file_name, 'w') as csv_file:
            field_names = [
                'LoanID',
                'Property',
                'Occupancy',
                'CITY',
                'STATE',
                'ZIP',
                'FICO',
                'Current_FICO_Score',
                'Current_Interest_Rate',
                'Original_Amount',
                'Original_Term',
                'Original_Appraisal_Amount',
                'Remaining_Term',
                'Amor_Term',
                'Current_Principal_Balance'
            ]
            writer = csv.DictWriter(csv_file, fieldnames=field_names)

            writer.writeheader()
            for i in range(loan_number):
                bank_loan_id = next_bank_loan_id(bank_loan_id)
                loan_dict = create_loan(bank_loan_id)
                writer.writerow(loan_dict)


if __name__ == '__main__':
    generate_loan_csv_files()
