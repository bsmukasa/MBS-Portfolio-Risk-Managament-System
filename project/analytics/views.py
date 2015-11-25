import pandas as pd
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from analytics.adjusted_assumptions_engine import generate_adjusted_assumptions
from analytics.cash_flows_engine import LoanPortfolio
from analytics.models import CashFlowsResults


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
        discount_rate = float(request_dict['discount_rate']) / 100

        analysis_results_name = "scenario_{}_portfolio_{}_discount_{}_analysis".format(scenario_id, portfolio_id,
                                                                                       discount_rate)
        cash_flow_results = self.model.objects.filter(
            scenario_id=scenario_id,
            portfolio_id=portfolio_id,
            analysis_results_name=analysis_results_name,
            discount_rate=discount_rate
        )

        if not cash_flow_results.exists():

            loan_df = generate_adjusted_assumptions(portfolio_id, scenario_id)

            loan_df.to_pickle(analysis_results_name + '_loans.pk')

            analysis_portfolio = LoanPortfolio(discount_rate=discount_rate, loan_df=loan_df)

            analysis_portfolio.cash_flows_df.to_pickle(analysis_results_name + '_cash_flows.pk')

            analysis_results = self.model(
                discount_rate=discount_rate,
                scenario_id=scenario_id,
                portfolio_id=portfolio_id,
                analysis_results_name=analysis_results_name)
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
        print("start")
        request_dict = request.GET.dict()

        scenario_id = request_dict['scenario_id']
        portfolio_id = request_dict['portfolio_id']
        discount_rate = float(request_dict['discount_rate']) / 100

        analysis_results_name = "scenario_{}_portfolio_{}_discount_{}_analysis".format(scenario_id, portfolio_id,
                                                                                       discount_rate)

        cash_flow_results = self.model.objects.filter(
            scenario_id=scenario_id,
            portfolio_id=portfolio_id,
            discount_rate=discount_rate,
            analysis_results_name=analysis_results_name
        )

        if cash_flow_results.exists():
            if not cash_flow_results[0].aggregated:
                loan_df = pd.read_pickle(analysis_results_name + '_loans.pk')
                cash_flow_df = pd.read_pickle(analysis_results_name + '_cash_flows.pk')

                analysis_portfolio = LoanPortfolio(
                    discount_rate=discount_rate, loan_df=loan_df, cash_flow_df=cash_flow_df
                )
                aggregate_cash_flow_df = analysis_portfolio.cash_flows_aggregate_for_portfolio()
                analysis_portfolio.cash_flows_df.to_pickle(analysis_results_name + '_aggregate_flows.pk')
                cash_flow_results[0].aggregated = True
                cash_flow_results[0].save()
            else:
                aggregate_cash_flow_df = pd.read_pickle(analysis_results_name + '_aggregate_flows.pk')

            aggregate_cash_flow = aggregate_cash_flow_df.to_json(orient="records")
            
            return JsonResponse(dict(aggregate_cash_flows=aggregate_cash_flow))


class AnalysisSummaryAPI(View):
    model = CashFlowsResults

    def dispatch(self, request, *args, **kwargs):
        return super(AnalysisSummaryAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        request_dict = request.GET.dict()

        scenario_id = request_dict['scenario_id']
        portfolio_id = request_dict['portfolio_id']
        discount_rate = float(request_dict['discount_rate']) / 100

        analysis_results_name = "scenario_{}_portfolio_{}_discount_{}_analysis".format(scenario_id, portfolio_id,
                                                                                       discount_rate)

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
            remaining_balance = analysis_portfolio.current_balance_aggregate_for_portfolio()
            npv = analysis_portfolio.net_present_value_aggregate_for_portfolio()


            #ERROR OCURRING HERE
            price = npv / analysis_portfolio.current_balance_aggregate_for_portfolio() * 100
            print("5")
            
            
            yield_irr = analysis_portfolio.internal_rate_of_return_aggregate_for_portfolio()
            weighted_average_life = analysis_portfolio.weighted_average_life_for_portfolio()
            original_cdr = analysis_portfolio.loan_df[0]['constant_default_rate']
            original_cpr = analysis_portfolio.loan_df[0]['constant_prepayment_rate']
            original_recovery = analysis_portfolio.loan_df[0]['recovery_percentage']
            weighted_average_cdr = analysis_portfolio.weighted_average_cdr_for_portfolio()
            weighted_average_cpr = analysis_portfolio.weighted_average_cpr_for_portfolio()
            weighted_average_recovery = analysis_portfolio.weighted_average_recovery_for_portfolio()
            return JsonResponse(dict(
                portfolio_balance=remaining_balance,
                npv=npv,
                price=price,
                yield_irr=yield_irr,
                weighted_average_life=weighted_average_life,
                original_cdr=original_cdr,
                original_cpr=original_cpr,
                original_recovery=original_recovery,
                weighted_average_cdr=weighted_average_cdr,
                weighted_average_cpr=weighted_average_cpr,
                weighted_average_recovery=weighted_average_recovery
            ))


class PrincipalGraphDataAPI(View):
    model = CashFlowsResults

    def dispatch(self, request, *args, **kwargs):
        return super(PrincipalGraphDataAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        request_dict = request.GET.dict()

        scenario_id = request_dict['scenario_id']
        portfolio_id = request_dict['portfolio_id']
        discount_rate = float(request_dict['discount_rate']) / 100

        analysis_results_name = "scenario_{}_portfolio_{}_discount_{}_analysis".format(scenario_id, portfolio_id,
                                                                                       discount_rate)

        cash_flow_results = self.model.objects.filter(
            scenario_id=scenario_id,
            portfolio_id=portfolio_id,
            discount_rate=discount_rate,
            analysis_results_name=analysis_results_name
        )

        if cash_flow_results.exists():
            aggregate_cash_flow_df = pd.read_pickle(analysis_results_name + '_aggregate_flows.pk')
            periods = list(aggregate_cash_flow_df['period'])
            scheduled_principals = list(aggregate_cash_flow_df['scheduled_principal'])
            unscheduled_principals = list(aggregate_cash_flow_df['unscheduled_principal'])
            principals_sums = list(
                aggregate_cash_flow_df['scheduled_principal'] + aggregate_cash_flow_df['unscheduled_principal']
            )

            return JsonResponse(dict(
                periods=periods,
                scheduled_principals=scheduled_principals,
                unscheduled_principals=unscheduled_principals,
                principals_sums=principals_sums
            ))
