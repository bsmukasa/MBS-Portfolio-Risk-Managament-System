import codecs
import csv
import datetime

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
        """ Gets all user's portfolios to show in dashboard.

        User must be logged.

        :param request: Request; must include name
        :return: Render dashboard
        """

        return render(request, self.template, {'form_upload': self.form_portfolio_tab,
                                               'form_assumptions': self.form_assumptions_tab,
                                               'choices': RiskFactor.RISK_FACTOR_ATTRIBUTE_CHOICES})


class PortfolioAPI(View):
    model = Portfolio

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PortfolioAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Gets all user's loan portfolios meeting given filter values in the request.GET.

        The active user is retrieved using the user_id stored in the session. If the user exists,
        use filter factors such as count for pagination or filter values to get relevant
        portfolios.

        User must be logged.

        :param request: Request; must include name
        :return: Json object with portfolios.
        """
        # TODO Uncomment next two lines and filter_dict['user'] when user app is installed and working.
        # user = get_user_model().objects.filter(pk=request.session['user_key'])
        # if user.exists():

        # Start Tab
        # filter_dict = request.GET.dict()
        # filter_dict['user'] = user
        # user_portfolios = self.model.objects.filter(**filter_dict).values()

        # Once with users delete this part and uncomment lines above
        user_portfolios = self.model.objects.all().values()

        return JsonResponse(dict(portfolios=list(user_portfolios)))
        # End Tab

    def post(self, request):
        """ Creates and saves a portfolio given a portfolio name.

        :param request: Request; must include portfolio name.
        """
        # TODO Uncomment next two lines and new_portfolio.user when user app is installed and working.
        # user = get_user_model().objects.filter(pk=request.session['user_key'])
        # if user.exists():

        # Start Tab
        form = FileForm(data=request.POST, files=request.FILES)

        if form.is_valid():

            form_dict = request.POST.dict()
            name = form_dict['name']

            new_portfolio = self.model(name=name)

            new_portfolio.total_loan_balance = 0
            new_portfolio.total_loan_count = 0
            new_portfolio.average_loan_balance = 0
            new_portfolio.weighted_average_coupon = 0
            new_portfolio.weighted_average_life_to_maturity = 0
            new_portfolio.save()

            # new_portfolio.user = user

            loan_list = []

            data = csv.DictReader(codecs.iterdecode(request.FILES['loan_file'], 'utf-8'))
            for row in data:
                loan = Loan(
                    portfolio=new_portfolio,
                    deferred_balance=is_set(row['DEFERRED_BAL']),
                    pmi_insurance=is_set(row['PMI']),
                    first_payment_date=convert_date_string(row['First_Payment_Date']),
                    junior_lien_balance=is_set(row['Junior Lien Bal']),
                    senior_lien_balance=is_set(row['Senior Lien Bal']),
                    mortgage_type=is_set(row['Mortgagetype']),
                    gross_margin=is_set(row['Gross_Margin']),
                    original_amount=is_set(row['Original_Amount']),
                    current_value_date=convert_date_string(row['Current_Value_Date']),
                    state=is_set(row['STATE']),
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
                    bank_loan_id=is_set(row['LoanID']),
                    second_lien_piggyback_flag=is_set(row['2nd Lien Piggyback Flag']),
                    junior_lien_balance_date=convert_date_string(row['Junior Lien Bal Date']),
                    first_index_rate_adjustment_date=convert_date_string(row['First_Interest_Rate_Adjustment_Date']),
                )
                loan_list.append(loan)

            Loan.objects.bulk_create(loan_list)

            saved_loans = Loan.objects.filter(portfolio=new_portfolio).values()
            portfolio_loans_calculations = calculate_aggregate_portfolio_data(saved_loans)

            new_portfolio.total_loan_balance = portfolio_loans_calculations['total_loan_balance']
            new_portfolio.total_loan_count = portfolio_loans_calculations['total_loan_count']
            new_portfolio.average_loan_balance = portfolio_loans_calculations['avg_loan_balance']
            new_portfolio.weighted_average_coupon = portfolio_loans_calculations['weighted_avg_coupon']
            new_portfolio.weighted_average_life_to_maturity = portfolio_loans_calculations[
                'weighted_avg_life_to_maturity']
            new_portfolio.save()
            # End Tab

            return JsonResponse({'status': 'OK', 'message': 'Risk Profile Created!!'})


class LoanPaginationAPI(View):
    model = Loan

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoanPaginationAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Gets all the loans from a selected portfolio in the session using
        filter values in the request.GET.

        Portfolio is retrieved using the portfolio_id stored in the session. If the portfolio exists,
        use filter factors such as a count of loans for pagination or field values to get loans
        meeting specific values.

        :param request: Request.
        :return: Json object with loans.
        """
        pagination_data = request.GET.dict()
        portfolio_id = pagination_data['portfolio_id']
        limit = int(pagination_data['limit'])
        offset = int(pagination_data['offset'])

        portfolio = Portfolio.objects.filter(pk=portfolio_id)
        loans = self.model.objects.filter(portfolio=portfolio)[offset:limit].values()
        total_count = self.model.objects.filter(portfolio=portfolio).count()

        return JsonResponse({"total": total_count, "rows": list(loans)})


class PortfolioView(View):
    template = "portfolio/portfolio.html"
    model = Portfolio

    def get(self, request, portfolio_id):
        """ Gets portfolio's information to show on page.

        User must be logged.

        :param request: Request; must include name; portfolio_id: Id of portfolio clicked
        :return: Render dashboard
        """
        portfolio = self.model.objects.filter(pk=portfolio_id).values()[0]
        portfolio['weighted_average_coupon'] *= 100
        return render(request, self.template, {"portfolio": portfolio})


class PortfolioStatusAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PortfolioStatusAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Gets all the loans from a selected portfolio in the session using
        filter values in the request.GET.

        Portfolio is retrieved using the portfolio_id stored in the session. If the portfolio exists,
        call helper function to calculate Current Balance and Loan Count for each possible loan status
        in the portfolio.
        Status choices: CURRENT, 90 DPD, FC, 60 DPD, REO, REPERF, 30 DPD, REM, CLAIM

        :param request: Request, portfolio_id
        :return: Json object with status summary.
        """
        request_data = request.GET.dict()
        portfolio_id = request_data['portfolio_id']

        portfolio = Portfolio.objects.get(pk=portfolio_id)
        loans = Loan.objects.filter(portfolio=portfolio).values()

        result = loans_status_summary(loans)

        return JsonResponse({'data': result}, safe=False)


class PortfolioFICOAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PortfolioFICOAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Gets all the loans from a selected portfolio in the session using
        filter values in the request.GET.

        Portfolio is retrieved using the portfolio_id stored in the session. If the portfolio exists,
        call helper function to calculate Current Balance and Loan Count for each possible loan status
        in the portfolio.
        Status choices: CURRENT, 90 DPD, FC, 60 DPD, REO, REPERF, 30 DPD, REM, CLAIM

        :param request: Request, portfolio_id
        :return: Json object with status summary.
        """
        request_data = request.GET.dict()
        portfolio_id = request_data['portfolio_id']

        portfolio = Portfolio.objects.get(pk=portfolio_id)
        loans = Loan.objects.filter(portfolio=portfolio).values()

        result = fico_summary(loans)

        return JsonResponse({'data': result}, safe=False)


# class LoanAdjustedAssumptionsAPI(View):
#     model = LoanAdjustedAssumptions
#
#     # TODO Determine how adjustments to loans are calculated, in aggregate or individually.
#     def post(self, request):
#         portfolio = Portfolio.objects.filter(pk=request.session['portfolio_id'])
#         if portfolio.exists():
#             filter_dict = request.GET.dict()
#             filter_dict['portfolio'] = portfolio
#             affected_loans = self.model.objects.filter(**filter_dict).values()


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

