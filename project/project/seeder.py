import csv
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import Loan, Portfolio
from risk_management.models import AssumptionProfile, RiskProfile, RiskFactor, RiskConditional
from portfolio.helper import calculate_aggregate_portfolio_data
from project.sample_loan_csv_creator import generate_loan_csv_files


def create_assumption_profiles():
    with open('assumptions_profiles.csv') as csv_file:
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
    with open('risk_profiles.csv') as csv_file:
        risk_profiles = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            risk_profiles.append(RiskProfile(name=row['name']))
        RiskProfile.objects.bulk_create(risk_profiles)


def create_risk_factors():
    with open('risk_factors.csv') as csv_file:
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
    with open('risk_conditionals.csv') as csv_file:
        risk_conditionals = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            risk_conditionals.append(RiskConditional(
                risk_factor_id=row['risk_factor_id'],
                conditional=row['conditional'],
                value=row['value']
            ))
        RiskConditional.objects.bulk_create(risk_conditionals)


def create_portfolios(loan_number_list):
    for loan_number in loan_number_list:
        loan_number_str = str(loan_number)
        file_name = loan_number_str + '_sample_loans.csv'
        portfolio_name = loan_number_str + ' Sample Loans'
        new_portfolio = Portfolio(
            name=portfolio_name
        )
        new_portfolio.total_loan_balance = 0
        new_portfolio.total_loan_count = 0
        new_portfolio.average_loan_balance = 0
        new_portfolio.weighted_average_coupon = 0
        new_portfolio.weighted_average_life_to_maturity = 0
        new_portfolio.save()

        with open(file_name) as csv_file:
            loans = []
            reader = csv.DictReader(csv_file)
            for row in reader:
                loans.append(Loan(
                    portfolio=new_portfolio,
                    bank_loan_id=row['LoanID'],
                    property_type_code=row['Property'],
                    occupancy_code=row['Occupancy'],
                    city=row['CITY'],
                    us_state=row['STATE'],
                    zipcode=row['ZIP'],
                    fico=row['FICO'],
                    current_FICO_score=row['Current_FICO_Score'],
                    current_interest_rate=row['Current_Interest_Rate'],
                    original_amount=row['Original_Amount'],
                    original_term=row['Original_Term'],
                    original_appraisal_amount=row['Original_Appraisal_Amount'],
                    remaining_term=row['Remaining_Term'],
                    amortized_term=row['Amor_Term'],
                    current_principal_balance=row['Current_Principal_Balance']
                ))
            Loan.objects.bulk_create(loans)

            saved_loans = Loan.objects.filter(portfolio=new_portfolio).values()
            portfolio_loans_calculations = calculate_aggregate_portfolio_data(saved_loans)

            new_portfolio.total_loan_balance = portfolio_loans_calculations['total_loan_balance']
            new_portfolio.total_loan_count = portfolio_loans_calculations['total_loan_count']
            new_portfolio.average_loan_balance = portfolio_loans_calculations['avg_loan_balance']
            new_portfolio.weighted_average_coupon = portfolio_loans_calculations['weighted_avg_coupon']
            new_portfolio.weighted_average_life_to_maturity = portfolio_loans_calculations[
                'weighted_avg_life_to_maturity']
            new_portfolio.save()


def reset_database():
    RiskConditional.objects.all().delete()
    RiskFactor.objects.all().delete()
    RiskProfile.objects.all().delete()
    Loan.objects.all().delete()
    Portfolio.objects.all().delete()
    AssumptionProfile.objects.all().delete()


if __name__ == '__main__':
    # Loan count for profiles to be created. Must correspond to csv file.
    loan_number_list = [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]

    print("Emptying Database...")
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
    print("Generating new loan csv files...")
    generate_loan_csv_files(loan_number_list)
    print("CSV Files generated....")
    create_portfolios(loan_number_list)
    print("Portfolios created...")
    print("Seeding complete...")
