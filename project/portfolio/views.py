import json
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from portfolio.models import Portfolio, Loan
from portfolio.forms import FileForm


# Create your views here.
class Dashboard(View):
    template = "portfolio/dashboard.html"
    form = FileForm

    def get(self, request):
        """ Gets all user's portfolios to show in dashboard.

        User must be logged.

        :param request: Request; must include name
        :return: Render dashboard
        """

        return render(request, self.template, {'form': self.form})


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
        filter_dict = request.GET.dict()
        # filter_dict['user'] = user
        user_portfolios = self.model.objects.filter(**filter_dict).values()


        #TO DELETE >> Test Values and Return
        portfolios = [
             {"name": "Wonder Years", 
                "total_loan_balance": 1000000, 
                "total_loan_count":200, 
                "average_loan_balance": 30000, 
                "weighted_average_coupon": 0.089, 
                "weighted_average_life_to_maturity": 255},
            {"name": "The OC", 
                "total_loan_balance": 50000000, 
                "total_loan_count":1000, 
                "average_loan_balance": 22000, 
                "weighted_average_coupon": 0.076, 
                "weighted_average_life_to_maturity": 321},              
            ]
        return JsonResponse({'portfolios': portfolios})


        #return JsonResponse(dict(portfolios=list(user_portfolios)))
        # End Tab

    def post(self, request):
        """ Creates and saves a portfolio given a portfolio name.

        :param request: Request; must include portfolio name.
        """
        # TODO Uncomment next two lines and new_portfolio.user when user app is installed and working.
        # user = get_user_model().objects.filter(pk=request.session['user_key'])
        # if user.exists():

        # Start Tab
        if request.method == 'POST':
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                form_dict = request.POST.dict()
                name = form_dict['name']

                new_portfolio = self.model(name=name)
                # new_portfolio.user = user

                # TODO Add loans to portfolio from csv file.
                new_portfolio.loan_file = request.FILES['loan_file']


                # TODO Calculate portfolio numbers from loaded loans.
                new_portfolio.total_loan_balance = 0
                new_portfolio.total_loan_count = 0
                new_portfolio.average_loan_balance = 0
                new_portfolio.weighted_average_coupon = 0
                new_portfolio.weighted_average_life_to_maturity = 0
                new_portfolio.save()
                # End Tab

                return redirect("/portfolio/dashboard")


class LoanAPI(View):
    model = Loan

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoanAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Gets all the loans from a selected portfolio in the session using
        filter values in the request.GET.

        Portfolio is retrieved using the portfolio_id stored in the session. If the portfolio exists,
        use filter factors such as a count of loans for pagination or field values to get loans
        meeting specific values.

        :param request: Request.
        :return: Json object with loans.
        """
        portfolio = Portfolio.objects.filter(pk=request.session['portfolio_id'])
        if portfolio.exists():
            filter_dict = request.GET.dict()
            filter_dict['portfolio'] = portfolio
            profile_loans = self.model.objects.filter(**filter_dict).values()
            return JsonResponse(dict(loans=list(profile_loans)))


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



