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

        analysis_results_name = "scenario_{}_portfolio_{}_discount_{}_analysis".format(
            scenario_id, portfolio_id, discount_rate
        )
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

            analysis_results = self.model.objects.create(
                discount_rate=discount_rate,
                scenario_id=scenario_id,
                portfolio_id=portfolio_id,
                analysis_results_name=analysis_results_name)
            analysis_results.save()

            message = 'New Analysis has been run.'
        else:
            message = 'Analysis has already been run.'
        return JsonResponse({'status': 'PASS', 'message': message})


def create_aggregate_cash_flows(analysis_results_name, cash_flow_results, discount_rate):
    loan_df = pd.read_pickle(analysis_results_name + '_loans.pk')
    cash_flow_df = pd.read_pickle(analysis_results_name + '_cash_flows.pk')
    analysis_portfolio = LoanPortfolio(
        discount_rate=discount_rate, loan_df=loan_df, cash_flow_df=cash_flow_df
    )
    aggregate_cash_flow_df = analysis_portfolio.cash_flows_aggregate_for_portfolio()
    analysis_portfolio.cash_flows_df.to_pickle(analysis_results_name + '_aggregate_flows.pk')
    cash_flow_results.aggregated = True
    cash_flow_results.save()
    return aggregate_cash_flow_df


class AggregateCashFlowsAPI(View):
    model = CashFlowsResults

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AggregateCashFlowsAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        request_dict = request.GET.dict()

        scenario_id = request_dict['scenario_id']
        portfolio_id = request_dict['portfolio_id']
        discount_rate = float(request_dict['discount_rate']) / 100

        analysis_results_name = "scenario_{}_portfolio_{}_discount_{}_analysis".format(
            scenario_id, portfolio_id, discount_rate
        )

        cash_flow_results = self.model.objects.filter(
            scenario_id=scenario_id,
            portfolio_id=portfolio_id,
            discount_rate=discount_rate,
            analysis_results_name=analysis_results_name
        )

        if cash_flow_results.exists():
            cash_flow_results = cash_flow_results[0]
            if not cash_flow_results.aggregated:
                aggregate_cash_flow_df = create_aggregate_cash_flows(
                    analysis_results_name, cash_flow_results, discount_rate
                )
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

        analysis_results_name = "scenario_{}_portfolio_{}_discount_{}_analysis".format(
            scenario_id, portfolio_id, discount_rate
        )

        cash_flow_results = self.model.objects.filter(
            scenario_id=scenario_id,
            portfolio_id=portfolio_id,
            discount_rate=discount_rate,
            analysis_results_name=analysis_results_name
        )

        if cash_flow_results.exists():
            cash_flow_results = cash_flow_results[0]
            loan_df = pd.read_pickle(analysis_results_name + '_loans.pk')
            cash_flow_df = pd.read_pickle(analysis_results_name + '_cash_flows.pk')

            if cash_flow_results.aggregated:
                aggregate_flows_df = pd.read_pickle(analysis_results_name + '_aggregate_flows.pk')
            else:
                aggregate_flows_df = create_aggregate_cash_flows(
                    analysis_results_name, cash_flow_results, discount_rate
                )

            analysis_portfolio = LoanPortfolio(
                discount_rate=discount_rate,
                loan_df=loan_df,
                cash_flow_df=cash_flow_df,
                aggregate_flows_df=aggregate_flows_df
            )

            remaining_balance = analysis_portfolio.current_balance_aggregate_for_portfolio()
            npv = analysis_portfolio.net_present_value_aggregate_for_portfolio()
            current_balance = analysis_portfolio.current_balance_aggregate_for_portfolio()
            price = npv / current_balance * 100
            yield_irr = float(analysis_portfolio.internal_rate_of_return_aggregate_for_portfolio()) * 100
            weighted_average_life = analysis_portfolio.weighted_average_life_for_portfolio()
            original_cdr = float(cash_flow_results.scenario.assumption_profile.constant_default_rate)
            original_cpr = float(cash_flow_results.scenario.assumption_profile.constant_prepayment_rate)
            original_recovery_percentage = float(cash_flow_results.scenario.assumption_profile.recovery_percentage)
            weighted_average_cdr = analysis_portfolio.weighted_average_cdr_for_portfolio()
            weighted_average_cpr = analysis_portfolio.weighted_average_cpr_for_portfolio()
            weighted_average_recovery = float(analysis_portfolio.weighted_average_recovery_for_portfolio()) * 100

            return JsonResponse(dict(
                portfolio_balance='$ {:,.2f}'.format(remaining_balance),
                npv='$ {:,.2f}'.format(npv),
                price='$ {:,.2f}'.format(price),
                yield_irr='{:.2%}'.format(yield_irr),
                weighted_average_life='{:,.2f}'.format(weighted_average_life),
                original_cdr='{:.2%}'.format(original_cdr),
                original_cpr='{:.2%}'.format(original_cpr),
                original_recovery='{:.2%}'.format(original_recovery_percentage),
                weighted_average_cdr='{:.2%}'.format(weighted_average_cdr),
                weighted_average_cpr='{:.2%}'.format(weighted_average_cpr),
                weighted_average_recovery='{:.2%}'.format(weighted_average_recovery)
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
            periods = [float(period) for period in list(aggregate_cash_flow_df['period'])]
            scheduled_principals = [
                float(sched_principal) for sched_principal in list(aggregate_cash_flow_df['scheduled_principal'])
                ]
            unscheduled_principals = [
                float(unsched_principal) for unsched_principal in list(aggregate_cash_flow_df['unscheduled_principal'])
                ]
            principals_sums = [
                float(principals_sum) for principals_sum in list(
                    aggregate_cash_flow_df['scheduled_principal'] + aggregate_cash_flow_df['unscheduled_principal']
                )
                ]
            return JsonResponse(dict(
                periods=periods,
                scheduled_principals=scheduled_principals,
                unscheduled_principals=unscheduled_principals,
                principals_sums=principals_sums
            ))
