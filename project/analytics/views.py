from analytics.cash_flows_engine import LoanPortfolio
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


class CashFlowsAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CashFlowsAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        filter_dict = request.GET.dict()
        loan_list = filter_dict['loan_list']

        analytics_portfolio = LoanPortfolio(loan_list)

        return JsonResponse(dict(cash_flows=analytics_portfolio.cash_flows_to_json()))
