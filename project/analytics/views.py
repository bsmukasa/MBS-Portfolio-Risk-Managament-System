import shelve

import pandas as pd
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from analytics.adjusted_assumptions_engine import generate_adjusted_assumptions
from analytics.cash_flows_engine import LoanPortfolio
from analytics.models import CashFlowsResults
from portfolio.models import Loan
from risk_management.models import ScoreCardProfile, ScoreCard, ScoreCardAttribute


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
            loan_df = generate_adjusted_assumptions(portfolio_id, scenario_id)
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
        portfolio_id = request_dict['portfolio_id']
        discount_rate = request_dict['discount_rate']
        adjusted_assumptions = generate_adjusted_assumptions(scenario_id, portfolio_id)

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


class ScoreCardProfileAPI(View):
    model = ScoreCardProfile

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ScoreCardProfileAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Get all saved score card profiles.

        Example Result:
            {
                "score_card_profiles": [
                    {
                        "name": "Defaults",
                        "date_created": "2015-10-30T21:06:42.621Z",
                        "last_updated": "2015-10-30T21:06:42.631Z"
                    },
                    {
                        "name": "Nintendo",
                        "date_created": "2015-10-30T21:06:42.621Z",
                        "last_updated": "2015-10-30T21:06:42.631Z"
                    },
                    {
                        "name": "Sony",
                        "date_created": "2015-10-30T21:06:42.621Z",
                        "last_updated": "2015-10-30T21:06:42.631Z"
                    }
                ]
            }

        :param request: Request
        return: JsonResponse list of assumption profiles on success, status and message if not.
        """
        filter_dict = request.GET.dict()
        score_card_profiles = self.model.objects.filter(**filter_dict).values()
        return JsonResponse(dict(score_card_profiles=list(score_card_profiles)))

    def post(self, request):
        """ Creates a new score card profile with default assumption score cards and saves it to the database.

        Creates default score cards for CDR, CPR, Recovery and Lag as well as score card attributes.

        Json in the Request must include:
        - name

        Example Request:
            {
                "name": "U.S. Economy Growing 3%"
            }

        :param request: Request.
        :return: JsonResponse with status and message.
        """
        request_data = request.POST.dict()
        name = request_data['name']

        score_card_profile = self.model(
            name=name
        )
        score_card_profile.save()

        card_list = []
        for choice in ScoreCard.ASSUMPTION_CHOICES:
            card = ScoreCard(
                score_card_profile=score_card_profile,
                assumption_type=choice[0]
            )
            card_list.append(card)

        ScoreCard.objects.bulk_create(card_list)

        card_list = ScoreCard.objects.filter(score_card_profile=score_card_profile)
        attributes = []
        for card in card_list:
            for choice in RiskFactor.RISK_FACTOR_ATTRIBUTE_CHOICES:
                weight = 100 / len(card_list)
                original_score = weight

                attributes.append(ScoreCardAttribute(
                    score_card=card,
                    attribute=choice,
                    weight=weight,
                    original_index=1,
                    original_score=original_score
                ))

        ScoreCardAttribute.objects.bulk_create(attributes)
        return JsonResponse({'status': 'OK', 'message': 'Score Card Profile Created!!'})


class ScoreCardAPI(View):
    model = ScoreCard

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ScoreCardAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Get all saved score cards associated with a score card profile.

        Example Result:
            {
                "score_cards": [
                    {
                        "score_card_profile_id": 2,
                        "assumption_type": "CDR"
                    },
                    {
                        "score_card_profile_id": 2,
                        "assumption_type": "CPR"
                    },
                    {
                        "score_card_profile_id": 2,
                        "assumption_type": "RECOV"
                    },
                    {
                        "score_card_profile_id": 2,
                        "assumption_type": "LAG"
                    }
                ]
            }

        :param request: Request
        return: JsonResponse list of score cards on success, status and message if not.
        """
        filter_dict = request.GET.dict()
        score_card_profile_id = filter_dict['score_card_profile_id']
        score_card_profile = ScoreCardProfile.objects.filter(pk=score_card_profile_id)

        if score_card_profile.exists():
            filter_dict['score_card_profile'] = score_card_profile

            score_cards = self.model.objects.filter(**filter_dict).values()

            pk_score_card = score_cards[1]["id"]
            scorecard_instance = ScoreCard.objects.filter(pk=pk_score_card)
            attributes = ScoreCardAttribute.objects.filter(score_card=scorecard_instance).values()

            return JsonResponse(dict(score_cards=list(score_cards), attributes=list(attributes)))
        else:
            return JsonResponse({'status': 'FAIL', 'message': 'Score Card Profile does not exist.'})


class ScoreCardAttributeAPI(View):
    model = ScoreCardAttribute

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ScoreCardAttributeAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        filter_dict = request.GET.dict()
        score_card_id = filter_dict['score_card_id']
        score_card = RiskFactor.objects.filter(pk=score_card_id)

        if score_card.exists():
            filter_dict['score_card'] = score_card

            attributes = self.model.objects.filter(**filter_dict).values()

            return JsonResponse(dict(attributes=list(attributes)))
        else:
            return JsonResponse({'status': 'FAIL', 'message': 'Score Card Profile does not exist.'})