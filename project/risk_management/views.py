import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from risk_management.models import RiskProfile, RiskFactor, RiskConditional, AssumptionProfile, ScoreCardProfile, \
    ScoreCard, ScoreCardAttribute


# Create your views here.
class RiskProfileAPI(View):
    model = RiskProfile

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RiskProfileAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Get all risk profiles.

        Request.GET may be used to add additional filter values.

        Example Results:
            {
                "risk_profiles": [
                    {
                        "id": 1,
                        "name": "Zipcode's in NJ",
                        "date_created": "2015-10-30T21:28:19.047Z",
                        "last_updated": "2015-10-30T21:28:19.047Z"
                    },
                    {
                        "id": 2,
                        name": "FICO Scores Above 500",
                        "date_created": "2015-09-23T21:29:19.895Z",
                        "last_updated": "2015-09-23T21:29:19.895Z"
                    },
                    {
                        "id": 4,
                        "name": "Current Interest Rate Above 6%",
                        "date_created": "2015-10-18T11:24:04.035Z",
                        "last_updated": "2015-10-30T21:38:41.035Z"
                    }
                ]
            }

        :param request: Request
        :return: JsonResponse list of risk profiles on success, status and message if not.
        """
        # Commented out for tests
        # filter_dict = request.GET.dict()
        # risk_profiles = self.model.objects.filter(**filter_dict).values()
        #
        #
        # return JsonResponse(dict(risk_profiles=list(risk_profiles)))

        # FOR TESTS >> DELETE later!
        teste = [
            {
                "id": 0,
                "name": "Zipcode in NY",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 1,
                "name": "FICO score above 700 in FL",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 2,
                "name": "Lien position 1",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 3,
                "name": "Zipcode in OH",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 4,
                "name": "Mortgage type FICO less 500",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 5,
                "name": "Zipcode in CA",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 6,
                "name": "Lien position 1",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 7,
                "name": "Zipcode in WA",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 8,
                "name": "Zipcode in NJ",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 9,
                "name": "FICO score above 500 in AZ",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 10,
                "name": "Zipcode in OR",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
            {
                "id": 11,
                "name": "FICO score above 600 in OR",
                "date_created": "2015-10-30T21:28:19.047Z",
                "last_updated": "2015-10-30T21:28:19.047Z"
            },
        ]

        return JsonResponse({'risk_profiles': teste})
        # END TEST

    def post(self, request):
        """ Creates a new risk profile and saves it to the database.

        Json in the Request must include:
        -name

        Example Request:
            {
                "name": Zipcode's in NJ
            }

        :param request: Request
        :return: JsonResponse including a status and message.
        """
        body = request.POST.dict()
        name = body['name']

        new_risk_profile = self.model(name=name)

        new_risk_profile.save()
        return JsonResponse({'status': 'OK', 'message': 'Risk Profile Created!!'})


class RiskFactorAPI(View):
    model = RiskFactor

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RiskFactorAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Get all risk factors related to a specific risk profile.

        Request.GET must include:
        -risk_profile_id

        Request.GET may be used to add additional filter values.

        Example Result:
            {
                "risk_factors": [
                    {
                        "id": 1,
                        "risk_profile_id": 2,
                        "attribute": "FICO",
                        "changing_assumption": "CDR",
                        "percentage_change": "-5.0000"
                    },
                    {
                        "id": 2,
                        "risk_profile_id": 2,
                        "attribute": "state",
                        "changing_assumption": "recovery",
                        "percentage_change": "2.0000"
                    }
                ]
            }

        :param request: Request
        :return: JsonResponse list of risk factors on success, status and message if not.
        """

        # Commented out for tests
        # filter_dict = request.GET.dict()

        # risk_profile_id = filter_dict['risk_profile_id']
        # risk_profile = RiskProfile.objects.filter(pk=risk_profile_id)

        # if risk_profile.exists():
        #     filter_dict['risk_profile'] = risk_profile

        #     risk_profile_risk_factors = self.model.objects.filter(**filter_dict).values()
        #     return JsonResponse(dict(risk_factors=list(risk_profile_risk_factors)))
        # else:
        #     return JsonResponse({'status': 'FAIL', 'message': 'Risk Profile provided does not exist.'})

        # TEST >> DELETE later
        teste = [
            {
                "risk_profile_id": 5,
                "risk_factor_id": 2,
                "attribute": "property_type",
                "changing_assumption": "cdr",
                "percentage_change": -5
            },
            {
                "risk_profile_id": 5,
                "risk_factor_id": 10,
                "attribute": "zipcode",
                "changing_assumption": "recovery",
                "percentage_change": -2
            },
            {
                "risk_profile_id": 5,
                "risk_factor_id": 12,
                "attribute": "FICO",
                "changing_assumption": "cpr",
                "percentage_change": 4
            }
        ]
        return JsonResponse({"risk_factors": teste})

    def post(self, request):
        """ Creates a new risk factor and related conditionals and saves it to the database.

        Json in the Request must include:
        - risk_profile_id
        - risk_factor_attribute
        - changing_assumption
        - percentage_change
        - conditionals_list

        Example Request:
            {
                "risk_profile_id": 2,
                "risk_factor_attribute": "FICO",
                "changing_assumption": "CDR",
                "percentage_change": -5,
                "conditionals_list": [
                    {"conditional": ">", "value": 450},
                    {"conditional": "<", "value": 550}
                ]
            }

        :param request: Request.
        :return: JsonResponse with status and message.
        """
        # filter_dict = request.GET.dict()
        body = request.POST.dict()

        if 'risk_profile_id' in body.keys():
            risk_profile_id = body['risk_profile_id']
            risk_profile = RiskProfile.objects.filter(pk=risk_profile_id)

            if risk_profile.exists():
                new_risk_factor = self.model()
                new_risk_factor.risk_profile = RiskProfile.objects.get(pk=risk_profile_id)
                new_risk_factor.attribute = body['risk_factor_attribute']
                new_risk_factor.changing_assumption = body['changing_assumption']
                new_risk_factor.percentage_change = body['percentage_change']
                new_risk_factor.save()

                conditionals_list = body['conditionals_list']
                print('Conditionals List:', conditionals_list)
                for item in conditionals_list:
                    new_risk_condtional = RiskConditional(risk_factor=new_risk_factor)
                    new_risk_condtional.conditional = item['conditional']
                    new_risk_condtional.value = item['value']
                    new_risk_condtional.save()

                return JsonResponse({'status': 'PASS', 'message': 'Risk Factor added.'})
            else:
                return JsonResponse({'status': 'FAIL', 'message': 'Risk Profile provided does not exist.'})
        else:
            return JsonResponse({'status': 'FAIL', 'message': 'Risk Profile ID must be provided.'})


class RiskConditionalAPI(View):
    model = RiskConditional

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RiskConditionalAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Get all saved risk conditionals related to a given risk factor.

        Request.GET must include:
        -risk_factor_id

        Example Result:
            {
                "risk_conditionals": [
                    {
                        "id": 1,
                        "risk_factor_id": 1,
                        "conditional": ">",
                        "value": "450"
                    },
                    {
                        "id": 2,
                        "risk_factor_id": 1,
                        "conditional": "<",
                        "value": 500
                    }
                ]
            }

        :param request: Request
        return: JsonResponse list of assumption profiles on success, status and message if not.
        """
        filter_dict = request.GET.dict()

        risk_factor_id = filter_dict['risk_factor_id']
        risk_factor = RiskFactor.objects.filter(pk=risk_factor_id)

        if risk_factor.exists():
            filter_dict['risk_factor'] = risk_factor

            risk_factor_conditionals = self.model.objects.filter(**filter_dict).values()

            return JsonResponse(dict(risk_conditionals=list(risk_factor_conditionals)))
        else:
            return JsonResponse({'status': 'FAIL', 'message': 'Risk Factor does not exist.'})


class AssumptionProfileAPI(View):
    model = AssumptionProfile

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AssumptionProfileAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Get all saved assumption profiles.

        Example Result:
            {
                "assumption_profiles": [
                    {
                        "national_home_price_index_growth": "3.7000",
                        "high_yield_spread": "5.2000",
                        "gdp_growth": 3,
                        "constant_default_rate": "8.0000",
                        "date_created": "2015-10-30T21:06:42.621Z",
                        "name": "3 Month Timber Shortage",
                        "constant_prepayment_rate": "21.4444",
                        "lag": "128.0000",
                        "last_updated": "2015-10-30T21:06:42.631Z",
                        "unemployment_rate": "8.5000",
                        "recovery": "59.2500",
                        "id": 1
                    },
                    {
                        "national_home_price_index_growth": "4.8000",
                        "high_yield_spread": "8.3000",
                        "gdp_growth": 4,
                        "constant_default_rate": "10.9800",
                        "date_created": "2015-10-30T21:16:06.398Z",
                        "name": "GDP Growing at 3%",
                        "constant_prepayment_rate": "17.2500",
                        "lag": "107.0000",
                        "last_updated": "2015-10-30T21:16:06.398Z",
                        "unemployment_rate": "8.5000",
                        "recovery": "-89.2300",
                        "id": 2
                    }
                ]
            }

        :param request: Request
        return: JsonResponse list of assumption profiles on success, status and message if not.
        """
        filter_dict = request.GET.dict()
        assumption_profiles = self.model.objects.filter(**filter_dict).values()
        return JsonResponse(dict(assumption_profiles=list(assumption_profiles)))

    def post(self, request):
        """ Creates a new assumption profile and saves it to the database.

        Json in the Request must include:
        - name
        - gdp_growth
        - unemployment_rate
        - national_home_price_index
        - high_yield_spread
        - constant_default_rate
        - constant_prepayment_rate
        - recovery
        - lag

        Example Request:
            {
                "name": "U.S. Economy Growing 3%",
                "gdp_growth": 3.2,
                "unemployment_rate": 8.5,
                "national_home_price_index_growth": 3.7,
                "high_yield_spread": 5.2,
                "constant_default_rate": -100,
                "constant_prepayment_rate": -100,
                "recovery": -100,
                "lag": 128
            }

        Default Assumptions, except for lag, may be sent as -100 to be calculated by the system or manually entered.

        All Economic Assumptions are given equal weight in calculation of Default Assumptions.

        Formulas:
            - CDR = (GDP * -1 + 6.5) + (Unemployment * 1.2 - 5.5)
            - CPR = YieldSpread * -10/9 + 245/9
            - Recovery = HPI * 2.5 + 50

        :param request: Request.
        :return: JsonResponse with status and message.
        """
        body = request.POST.dict()
        name = body['name']
        gdp_growth = body['gdp_growth']
        unemployment_rate = body['unemployment_rate']
        national_home_price_index = body['national_home_price_index']
        high_yield_spread = body['high_yield_spread']

        new_assumption_profile = self.model(
            name=name,
            gdp_growth=gdp_growth,
            unemployment_rate=unemployment_rate,
            national_home_price_index_growth=national_home_price_index,
            high_yield_spread=high_yield_spread
        )

        default_assumptions = {
            "constant_default_rate": body['constant_default_rate'],
            "constant_prepayment_rate": body['constant_prepayment_rate'],
            "recovery": body['recovery'],
            "lag": body['lag']
        }

        for key, value in default_assumptions.items():
            if value != -100:
                setattr(new_assumption_profile, key, value)
            else:
                if key == 'constant_default_rate':
                    cdr = (gdp_growth * -1 + 6.5)
                    cdr += (unemployment_rate * 1.2 - 5.5)
                    new_assumption_profile.constant_default_rate = cdr
                if key == 'constant_prepayment_rate':
                    cpr = high_yield_spread * -10 / 9 + 245 / 9
                    new_assumption_profile.constant_prepayment_rate = cpr
                if key == 'recovery':
                    recovery = national_home_price_index * 2.5 + 50
                    new_assumption_profile.recovery = recovery
                if key == 'lag':
                    lag = value
                    new_assumption_profile.lag = lag

        new_assumption_profile.save()
        return JsonResponse({'status': 'OK', 'message': 'Assumption Profile Created!!'})


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
        body = request.POST.dict()
        name = body['name']

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
        score_card_profile = RiskFactor.objects.filter(pk=score_card_profile_id)

        if score_card_profile.exists():
            filter_dict['score_card_profile'] = score_card_profile

            score_cards = self.model.objects.filter(**filter_dict).values()

            return JsonResponse(dict(score_cards=list(score_cards)))
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
