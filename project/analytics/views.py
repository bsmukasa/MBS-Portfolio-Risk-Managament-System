import shelve

import pandas as pd
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from analytics.adjusted_assumptions_engine import get_adjusted_assumptions
from analytics.cash_flows_engine import LoanPortfolio
from analytics.models import CashFlowsResults
from portfolio.models import Loan


class CashFlowsAPI(View):
    model = CashFlowsResults

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CashFlowsAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        """ Conducts new analysis on portfolio, scenario combinations.

        If cash_flow_results do not exist with the same scenario_id, portfolio_id and analysis_results_name,
        a new cash flow is generated.

        Args:
            request: Request

        Returns: Status and message indicating if there it is a new analysis.

        """
        request_dict = request.POST.dict()

        scenario_id = request_dict['scenario_id']
        portfolio_id = request_dict['portfolio_id']
        discount_rate = request_dict['discount_rate']

        analysis_results_name = "scenario_{}_portfolio_{}_analysis".format(scenario_id, portfolio_id)

        cash_flow_results = self.model.objects.filter(
            scenario_id=scenario_id,
            portfolio_id=portfolio_id,
            analysis_results_name=analysis_results_name
        )

        if not cash_flow_results.exists():
            loan_df = pd.DataFrame(list(Loan.objects.filter(portfolio_id=portfolio_id)))
            loan_df.to_pickle(analysis_results_name + '_loans.pk')

            analysis_portfolio = LoanPortfolio(discount_rate=discount_rate, loan_df=loan_df)
            analysis_portfolio.cash_flows_df.to_pickle(analysis_results_name + '_cash_flows.pk')

            analysis_results = self.model(
                scenario_id=scenario_id,
                portfolio_id=portfolio_id,
                analysis_results_file_name=analysis_results_name)
            analysis_results.save()

            message = 'New Analysis has been run.'
        else:
            message = 'Analysis has already been run.'

        return JsonResponse({'status': 'PASS', 'message': message})


class AggregateCashFlowsAPI(View):
    model = CashFlowsResults

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AggregateCashFlowsAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        request_dict = request.GET.dict()

        scenario_id = request_dict['scenario_id']
        portfolio_id = request_dict['scenario_id']
        discount_rate = request_dict['discount_rate']
        adjusted_assumptions = get_adjusted_assumptions(scenario_id, portfolio_id)

        analysis_results_name = "scenario_{}_portfolio_{}_analysis".format(scenario_id, portfolio_id)

        cash_flow_results = self.model.objects.filter(
            scenario_id=scenario_id,
            portfolio_id=portfolio_id,
            discount_rate=discount_rate,
            analysis_results_name=analysis_results_name
        )

        if cash_flow_results.exists():
            loan_df = pd.read_pickle(analysis_results_name + '_loans.pk')
            cash_flow_df = pd.read_pickle(analysis_results_name + '_cash_flows.pk')

            analysis_portfolio = LoanPortfolio(discount_rate=discount_rate, loan_df=loan_df, cash_flow_df=cash_flow_df)
            aggregate_cash_flow_df = analysis_portfolio.cash_flows_aggregate_for_portfolio()
            aggregate_cash_flow = aggregate_cash_flow_df.to_json(orient="records")
            return JsonResponse(dict(aggregate_cash_flows=list(aggregate_cash_flow)))
