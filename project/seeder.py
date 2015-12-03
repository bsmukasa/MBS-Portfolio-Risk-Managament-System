import csv
import os
import random

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import Loan, Portfolio
from risk_management.models import AssumptionProfile, RiskProfile, RiskFactor, RiskConditional
from portfolio.helper import calculate_aggregate_portfolio_data, fico_summary, loans_status_summary
from portfolio.views import is_set, convert_date_string


def create_assumption_profiles():
    with open('seeder_csv_files/assumptions_profiles.csv') as csv_file:
        assumption_profiles = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            assumption_profiles.append(AssumptionProfile(
                name=row['name'],
                gdp_growth=row['gdp_growth'],
                unemployment_rate=row['unemployment_rate'],
                national_home_price_index_growth=row['national_home_price_index_growth'],
                high_yield_spread=row['high_yield_spread'],
                constant_default_rate=row['constant_default_rate'],
                constant_prepayment_rate=row['constant_prepayment_rate'],
                recovery_percentage=row['recovery_percentage']
            ))
        AssumptionProfile.objects.bulk_create(assumption_profiles)


def create_risk_profiles():
    with open('seeder_csv_files/risk_profiles.csv') as csv_file:
        risk_profiles = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            risk_profiles.append(RiskProfile(name=row['name']))
        RiskProfile.objects.bulk_create(risk_profiles)


def create_risk_factors():
    with open('seeder_csv_files/risk_factors.csv') as csv_file:
        risk_factors = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            risk_factors.append(RiskFactor(
                risk_profile_id=row['risk_profile_id'],
                attribute=row['attribute'],
                changing_assumption=row['changing_assumption'],
                percentage_change=row['percentage_change']
            ))
        RiskFactor.objects.bulk_create(risk_factors)


def create_risk_conditionals():
    with open('seeder_csv_files/risk_conditionals.csv') as csv_file:
        risk_conditionals = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            risk_conditionals.append(RiskConditional(
                risk_factor_id=row['risk_factor_id'],
                conditional=row['conditional'],
                value=row['value']
            ))
        RiskConditional.objects.bulk_create(risk_conditionals)


def next_bank_loan_id(last_id=None):
    return last_id + random.randint(151, 1127)


def create_portfolios(loan_number_list):
    print('Portfolio started....')
    for loan_number in loan_number_list:
        loan_number_str = str(loan_number)
        portfolio_name = loan_number_str + ' Sample Loans'
        new_portfolio = Portfolio(
            name=portfolio_name
        )
        new_portfolio.save()

        bank_loan_id = random.randint(500000, 600000)

        loans = []
        # file_name = loan_number_str + '_sample_loans.csv'

        while len(loans) < loan_number:
            start_row = random.randint(0, 3000)

            real_world_file_number_str = str(random.randint(1, 7))
            real_world_file_name = 'real_world_data/5000_real_world_loans_' + real_world_file_number_str + '.csv'
            with open(real_world_file_name) as real_world_csv_file:
                reader = csv.DictReader(real_world_csv_file)
                for row in reader:
                    if start_row == 0 and len(loans) < loan_number:
                        bank_loan_id = next_bank_loan_id(bank_loan_id)
                        loans.append(Loan(
                            portfolio=new_portfolio,
                            bank_loan_id=bank_loan_id,
                            deferred_balance=is_set(row['DEFERRED_BAL']),
                            pmi_insurance=is_set(row['PMI']),
                            first_payment_date=convert_date_string(row['First_Payment_Date']),
                            junior_lien_balance=is_set(row['Junior Lien Bal']),
                            senior_lien_balance=is_set(row['Senior Lien Bal']),
                            mortgage_type=is_set(row['Mortgagetype']),
                            gross_margin=is_set(row['Gross_Margin']),
                            original_amount=is_set(row['Original_Amount']),
                            current_value_date=convert_date_string(row['Current_Value_Date']),
                            us_state=is_set(row['STATE']),
                            BK_flag=is_set(row['BK_FLAG']),
                            negam_initial_minimum_payment_period=is_set(row['Negam_Initial_Minimum_Payment_Period']),
                            product_type=is_set(row['Product_Type']),
                            remaining_term=is_set(row['Remaining_Term']),
                            first_recast_or_next_recast=is_set(row['First_Recast/Next_Recast']),
                            amortized_term=is_set(row['Amor_Term']),
                            recast_cap=is_set(row['Recast_Cap']),
                            occupancy_code=is_set(row['Occupancy']),
                            modification_date=convert_date_string(row['Modification_Date']),
                            negam_payment_reset_frequency=is_set(row['Negam_Payment_Reset_Frequency']),
                            IO_term=is_set(row['IO_Term']),
                            senior_lien_balance_date=convert_date_string(row['Senior Lien Bal Date']),
                            icap=is_set(row['ICAP']),
                            current_interest_rate=is_set(row['Current_Interest_Rate']),
                            SF=is_set(row['SF']),
                            fico=is_set(row['FICO']),
                            pcap=is_set(row['PCAP']),
                            interest_reset_interval=is_set(row['Interest_Reset_Interval']),
                            recast_frequency=is_set(row['Recast_Frequency']),
                            original_term=is_set(row['Original_Term']),
                            as_of_date=convert_date_string(row['AS_OF_DATE']),
                            lcap=is_set(row['LCAP']),
                            status=is_set(row['STATUS']),
                            MSR=is_set(row['MSR']),
                            original_appraisal_amount=is_set(row['Original_Appraisal_Amount']),
                            lfloor=is_set(row['LFLOOR']),
                            purpose=is_set(row['Purpose']),
                            reset_index=is_set(row['Reset_Index']),
                            zipcode=is_set(row['ZIP']),
                            property_type_code=is_set(row['Property']),
                            lien_position=is_set(row['Lien_Position']),
                            current_FICO_score=is_set(row['Current_FICO_Score']),
                            current_property_value=is_set(row['Current_Property_Value']),
                            foreclosure_referral_date=convert_date_string(row['Foreclosure_Referral_Date']),
                            current_principal_balance=is_set(row['Current_Principal_Balance']),
                            last_payment_received=convert_date_string(row['LAST_PMT_RECD']),
                            original_rate=is_set(row['ORATE']),
                            original_date=convert_date_string(row['Origination_Date']),
                            city=is_set(row['CITY']),
                            second_lien_piggyback_flag=is_set(row['2nd Lien Piggyback Flag']),
                            junior_lien_balance_date=convert_date_string(row['Junior Lien Bal Date']),
                            first_index_rate_adjustment_date=convert_date_string(
                                row['First_Interest_Rate_Adjustment_Date']
                            )
                        ))
                    else:
                        start_row -= 1

        Loan.objects.bulk_create(loans)

        saved_loans = Loan.objects.filter(portfolio=new_portfolio).values()
        portfolio_loans_calculations = calculate_aggregate_portfolio_data(saved_loans)

        new_portfolio.total_loan_balance = portfolio_loans_calculations['total_loan_balance']
        new_portfolio.total_loan_count = portfolio_loans_calculations['total_loan_count']
        new_portfolio.average_loan_balance = portfolio_loans_calculations['avg_loan_balance']
        new_portfolio.weighted_average_coupon = portfolio_loans_calculations['weighted_avg_coupon']
        new_portfolio.weighted_average_life_to_maturity = portfolio_loans_calculations[
            'weighted_avg_life_to_maturity']

        # Loan status summary data
        loan_status_summary = loans_status_summary(saved_loans)
        new_portfolio.current_balance = loan_status_summary["CURRENT"]["balance"]
        new_portfolio.current_count = loan_status_summary["CURRENT"]["count"]
        new_portfolio.dpd90_balance = loan_status_summary["90 DPD"]["balance"]
        new_portfolio.dpd90_count = loan_status_summary["90 DPD"]["count"]
        new_portfolio.fc_balance = loan_status_summary["FC"]["balance"]
        new_portfolio.fc_count = loan_status_summary["FC"]["count"]
        new_portfolio.dpd60_balance = loan_status_summary["60 DPD"]["balance"]
        new_portfolio.dpd60_count = loan_status_summary["60 DPD"]["count"]
        new_portfolio.reo_balance = loan_status_summary["REO"]["balance"]
        new_portfolio.reo_count = loan_status_summary["REO"]["count"]
        new_portfolio.reperf_balance = loan_status_summary["REPERF"]["balance"]
        new_portfolio.reperf_count = loan_status_summary["REPERF"]["count"]
        new_portfolio.dpd30_balance = loan_status_summary["30 DPD"]["balance"]
        new_portfolio.dpd30_count = loan_status_summary["30 DPD"]["count"]
        new_portfolio.rem_balance = loan_status_summary["REM"]["balance"]
        new_portfolio.rem_count = loan_status_summary["REM"]["count"]
        new_portfolio.claim_balance = loan_status_summary["CLAIM"]["balance"]
        new_portfolio.claim_count = loan_status_summary["CLAIM"]["count"]

        # FICO summary data
        fico_results = fico_summary(saved_loans)
        new_portfolio.max_fico = fico_results["max_fico"]
        new_portfolio.min_fico = fico_results["min_fico"]
        new_portfolio.weighted_average_fico = fico_results["wa_fico"]
        print('Portfolio created...')
        new_portfolio.save()


def reset_database():
    RiskConditional.objects.all().delete()
    RiskFactor.objects.all().delete()
    RiskProfile.objects.all().delete()
    Loan.objects.all().delete()
    Portfolio.objects.all().delete()
    AssumptionProfile.objects.all().delete()


if __name__ == '__main__':
    # Loan count for profiles to be created.
    loan_number_list = [1000, 100, 25, 500]

    reset_database()
    print("Database Rest...")
    print("Starting seed script...")
    create_assumption_profiles()
    print("Assumptions created...")
    create_risk_profiles()
    print("Risk profiles created...")
    create_risk_factors()
    print("Risk factors created...")
    create_risk_conditionals()
    print("Risk conditionals created...")
    print("Creating Portfolios...")
    create_portfolios(loan_number_list)
    print("Portfolios created...")
    print("Seeding complete...")
