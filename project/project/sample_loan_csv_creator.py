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
        bank_loan_id=loan_id,
        property_type_code=property_type_code,
        occupancy_code='AB',
        city=address[1],
        us_state=address[2],
        zipcode=address[0],
        # as_of_date=,
        # first_payment_date=,
        # original_date=,
        # first_index_rate_adjustment_date=,
        fico=fico,
        current_FICO_score=current_fico,
        current_interest_rate=current_interest_rate,
        original_amount=original_amount,
        original_term=original_term,
        original_appraisal_amount=original_appraisal_amount,
        remaining_term=remaining_term,
        amortized_term=amortized_term,
        current_principal_balance=current_principal_balance,
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

if __name__ == '__main__':
    bank_loan_id = random.randint(500000, 600000)
    with open('30000_sample_loans.csv', 'w') as csv_file:
        field_names = [
            'bank_loan_id',
            'property_type_code',
            'occupancy_code',
            'city',
            'us_state',
            'zipcode',
            'fico',
            'current_FICO_score',
            'current_interest_rate',
            'original_amount',
            'original_term',
            'original_appraisal_amount',
            'remaining_term',
            'amortized_term',
            'current_principal_balance'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        writer.writeheader()
        for i in range(30000):
            bank_loan_id = next_bank_loan_id(bank_loan_id)
            loan_dict = create_loan(bank_loan_id)
            writer.writerow(loan_dict)
