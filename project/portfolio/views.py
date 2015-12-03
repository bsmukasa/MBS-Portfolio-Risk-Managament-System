import codecs
import csv
import datetime
import random

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from portfolio.helper import calculate_aggregate_portfolio_data, loans_status_summary, fico_summary
from portfolio.models import Portfolio, Loan
from risk_management.forms import AssumptionForm
from risk_management.models import RiskFactor
# Check if its needed and saves correctly
from portfolio.forms import FileForm


# Create your views here.
class DashboardView(View):
    template = "portfolio/dashboard.html"
    form_portfolio_tab = FileForm
    form_assumptions_tab = AssumptionForm

    def get(self, request):
        return render(request, self.template, {'form_upload': self.form_portfolio_tab,
                                               'form_assumptions': self.form_assumptions_tab,
                                               'choices': RiskFactor.RISK_FACTOR_ATTRIBUTE_CHOICES})


class PortfolioAPI(View):
    model = Portfolio

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PortfolioAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        user_portfolios = self.model.objects.all()

        portfolios = []
        for portfolio in user_portfolios:
            portfolios.append(
                {
                    'total_loan_balance': convert_decimal_to_currency(portfolio.total_loan_balance),
                    'total_loan_count': convert_int_with_commas(portfolio.total_loan_count),
                    'average_loan_balance': convert_decimal_to_currency(portfolio.average_loan_balance),
                    'weighted_average_coupon': '{:.2%}'.format(portfolio.weighted_average_coupon),
                    'weighted_average_life_to_maturity': convert_decimal_to_currency(
                        portfolio.weighted_average_life_to_maturity)
                }
            )

        return JsonResponse(dict(portfolios=list(user_portfolios)))

    def post(self, request):
        form = FileForm(data=request.POST, files=request.FILES)

        if form.is_valid():

            form_dict = request.POST.dict()
            name = form_dict['name']

            new_portfolio = self.model(name=name)
            new_portfolio.save()

            bank_loan_id = random.randint(300000, 800000)
            loans = []

            data = csv.DictReader(codecs.iterdecode(request.FILES['loan_file'], 'utf-8'))
            for row in data:
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

            Loan.objects.bulk_create(loans)

            saved_loans = Loan.objects.filter(portfolio=new_portfolio).values()
            portfolio_loans_calculations = calculate_aggregate_portfolio_data(saved_loans)

            # Aggregate summary data
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

            new_portfolio.save()

            return JsonResponse({'status': 'OK', 'message': 'Risk Profile Created!!'})


def next_bank_loan_id(last_id=None):
    return last_id + random.randint(151, 1127)


class LoanPaginationAPI(View):
    model = Loan

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoanPaginationAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        pagination_data = request.GET.dict()
        portfolio_id = pagination_data['portfolio_id']
        limit = int(pagination_data['limit'])
        offset = int(pagination_data['offset'])

        portfolio = Portfolio.objects.filter(pk=portfolio_id)
        loans = self.model.objects.filter(portfolio=portfolio)[offset:limit].values()
        total_count = self.model.objects.filter(portfolio=portfolio).count()

        return JsonResponse({"total": total_count, "rows": list(loans)})


class PortfolioView(View):
    model = Portfolio
    template = "portfolio/portfolio.html"

    def get(self, request, portfolio_id):
        portfolio = self.model.objects.get(pk=portfolio_id)
        portfolio = {
            'total_loan_balance': convert_decimal_to_currency(portfolio.total_loan_balance),
            'total_loan_count': portfolio.total_loan_count,
            'average_loan_balance': convert_decimal_to_currency(portfolio.average_loan_balance),
            'weighted_average_coupon': '{:.2%}'.format(portfolio.weighted_average_coupon),
            'weighted_average_life_to_maturity': convert_decimal_to_currency(
                portfolio.weighted_average_life_to_maturity
            )
        }
        return render(request, self.template, {"portfolio": portfolio})


class PortfolioStatusAPI(View):
    model = Portfolio

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PortfolioStatusAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        request_data = request.GET.dict()
        portfolio = self.model.objects.get(pk=request_data['portfolio_id'])

        result = [
            {
                "status": "CURRENT",
                "balance": convert_decimal_to_currency(portfolio.current_balance),
                "count": portfolio.current_count
            },
            {
                "status": "90 DPD",
                "balance": convert_decimal_to_currency(portfolio.dpd90_balance),
                "count": portfolio.dpd90_count
            },
            {
                "status": "FC",
                "balance": convert_decimal_to_currency(portfolio.fc_balance),
                "count": portfolio.fc_count
            },
            {
                "status": "60 DPD",
                "balance": convert_decimal_to_currency(portfolio.dpd60_balance),
                "count": portfolio.dpd60_count},
            {
                "status": "REO",
                "balance": convert_decimal_to_currency(portfolio.reo_balance),
                "count": portfolio.reo_count
            },
            {
                "status": "REPERF",
                "balance": convert_decimal_to_currency(portfolio.reperf_balance),
                "count": portfolio.reperf_count
            },
            {
                "status": "30 DPD",
                "balance": convert_decimal_to_currency(portfolio.dpd30_balance),
                "count": portfolio.dpd30_count
            },
            {
                "status": "REM",
                "balance": convert_decimal_to_currency(portfolio.rem_balance),
                "count": portfolio.rem_count
            },
            {
                "status": "CLAIM",
                "balance": convert_decimal_to_currency(portfolio.claim_balance),
                "count": portfolio.claim_count
            }
        ]

        return JsonResponse({'data': result}, safe=False)


def convert_decimal_to_currency(decimal_number):
    float_number = float(decimal_number)
    return '{:.2%}'.format(float_number)


def convert_int_with_commas(db_int_number):
    int_number = int(db_int_number)
    return '{:,}'.format(int_number)


def convert_decimal_to_percentage(decimal_number):
    float_number = float(decimal_number)
    return '{:.2%}'.format(float_number)


class PortfolioFICOAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PortfolioFICOAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        request_data = request.GET.dict()
        portfolio_id = request_data['portfolio_id']

        portfolio = Portfolio.objects.get(pk=portfolio_id)
        result = [
            {
                "max_fico": portfolio.max_fico,
                "min_fico": portfolio.min_fico,
                "wa_fico": portfolio.weighted_average_fico
            }
        ]

        return JsonResponse({'data': result}, safe=False)


def convert_date_string(date_string):
    if date_string == '':
        return None
    else:
        parse_date = datetime.datetime.strptime(date_string, '%m/%d/%y').date()
        return parse_date


def is_set(field):
    if not field:
        return None
    return field

