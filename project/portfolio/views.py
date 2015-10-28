from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.generic import View
from portfolio.models import Portfolio, Loan


# Create your views here.
class PortfolioAPI(View):
    model = Portfolio

    def get(self, request):
        user = get_user_model().objects.filter(pk=request.session['user_key'])
        if user.exists():
            filter_dict = request.GET.dict()
            filter_dict['user'] = user
            user_portfolios = self.model.objects.filter(**filter_dict).values()
            return JsonResponse(dict(profiles=list(user_portfolios)))


class LoanAPI(View):
    model = Loan

    def get(self, request):
        portfolio = Portfolio.objects.filter(pk=request.session['portfolio_id'])
        if portfolio.exists():
            filter_dict = request.GET.dict()
            filter_dict['portfolio'] = portfolio
            profile_loans = self.model.objects.filter(**filter_dict).values()
            return JsonResponse(dict(loans=list(profile_loans)))
