import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from risk_management.models import RiskProfile, RiskFactor, RiskConditional, AssumptionProfile



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
                "risk_profile_list": {
                    "risk_profile": [
                        {
                            "risk_profile_id": 3,
                            "name": "NJ Zipcodes",
                            "date_created": "2015-07-12",
                            "last_updated": "2015-08-29"
                        },
                        {
                            "risk_profile_id": 7,
                            name": "Second Residence Homes",
                            "date_created": "2015-09-23",
                            "last_updated": "2015-09-23"
                        },
                        {
                            "risk_profile_id": 22,
                            "name": "East Coast States",
                            "date_created": "2015-10-12",
                            "last_updated": "2015-10-18"
                        }
                    ]
                }
            }

        :param request: Request
        :return: JsonResponse list of risk profiles on success, status and message if not.
        """
        filter_dict = request.GET.dict()
        risk_profiles = self.model.objects.filter(**filter_dict).values()

        #Commented for tests
        # return JsonResponse(dict(risk_profiles=list(risk_profiles)))


        #FOR TESTS >> DELETE later!
        teste = [
            { 
                "id": 0,
                "name": "Zipcode in NY"
            },
            { 
                "id": 1,
                "name": "FICO score above 700 in FL"
            },
                        { 
                "id": 2,
                "name": "Lien position 1"
            },
                        { 
                "id": 3,
                "name": "Zipcode in OH"
            },
                        { 
                "id": 4,
                "name": "Mortgage type FICO less 500"
            },
                        { 
                "id": 5,
                "name": "Zipcode in CA"
            },
                        { 
                "id": 6,
                "name": "Lien position 1"
            },
                        { 
                "id": 7,
                "name": "Zipcode in WA"
            },
                        { 
                "id": 8,
                "name": "Zipcode in NJ"
            },
                        { 
                "id": 9,
                "name": "FICO score above 500 in AZ"
            },
                        { 
                "id": 10,
                "name": "Zipcode in OR"
            },
                        { 
                "id": 11,
                "name": "FICO score above 600 in OR"
            },
        ]

        return JsonResponse({'risk_profiles': teste})
        #END TEST

        

    def post(self, request):
        """ Creates a new risk profile and saves it to the database.

        Json in the Request must include:
        -name

        Example Request:
            {
                "risk_profile": {"name": Zipcode's in NJ}
            }

        :param request: Request
        :return: JsonResponse including a status and message.
        """
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
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

        Request.GET may be used to add additional filter values.

        Json in the Request must include:
        -risk_profile_id

        Example Request:
            {
                "risk_profile_search_terms": {"risk_profile_id": 5}
            }

        Example Result:
            {
                "risk_factor_list": {
                    "risk_factor": [
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
                }
            }

        :param request: Request
        :return: JsonResponse list of risk factors on success, status and message if not.
        """
        filter_dict = request.GET.dict()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if 'risk_profile_id' in body.keys():
            risk_profile_id = body['risk_profile_id']
            risk_profile = RiskProfile.objects.filter(pk=risk_profile_id)

            if risk_profile.exists():
                filter_dict['risk_profile'] = risk_profile

                risk_profile_risk_factors = self.model.objects.filter(**filter_dict).values()
                return JsonResponse(dict(risk_factors=list(risk_profile_risk_factors)))
            else:
                return JsonResponse({'status': 'FAIL', 'message': 'Risk Profile provided does not exist.'})
        else:
            return JsonResponse({'status': 'FAIL', 'message': 'Risk Profile ID must be provided.'})

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
                "risk_factor": {
                    "risk_profile_id": 5,
                    "risk_factor_attribute": "FICO",
                    "changing_assumption": "CDR",
                    "percentage_change": -5,
                    "conditionals_list": {
                        "conditional_item": [
                            {"conditional": ">", "value": 450},
                            {"conditional": "<", "value": 550}
                        ]
                    }
                }
            }

        :param request: Request.
        :return: JsonResponse with status and message.
        """
        # filter_dict = request.GET.dict()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if 'risk_profile_id' in body.keys():
            risk_profile_id = body['risk_profile_id']
            risk_profile = RiskProfile.objects.filter(pk=risk_profile_id)

            if risk_profile.exists():
                new_risk_factor = self.model(risk_profile=risk_profile)
                new_risk_factor.attribute = body['risk_factor_attribute']
                new_risk_factor.changing_assumption = body['changing_assumption']
                new_risk_factor.percentage_change = body['percentage_change']

                conditionals_list = body['conditionals_list']
                for item in conditionals_list:
                    new_risk_condtional = RiskConditional(risk_factor=new_risk_factor)
                    new_risk_condtional.conditional = item['conditional']
                    new_risk_factor.value = item['value']

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

        Json in the Request must include:
        -risk_factor_id

        Example Request:
            {
                "risk_conditional_search_terms": {"risk_factor_id": 3}
            }

        Example Result:
            {
                "risk_conditional_list": {
                    "risk_conditional": [
                        {
                            "risk_factor_id": 10,
                            "risk_conditional_id": 4,
                            "conditional": ">",
                            "value": 500
                        },
                        {
                            "risk_factor_id": 10,
                            "risk_conditional_id": 5,
                            "conditional": "<",
                            "value": 700
                        }
                    ]
                }
            }

        :param request: Request
        return: JsonResponse list of assumption profiles on success, status and message if not.
        """
        filter_dict = request.GET.dict()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if 'risk_profile_id' in body.keys() and 'risk_factor_id' in body.keys():
            risk_profile_id = body['risk_profile_id']
            risk_profile = RiskProfile.objects.filter(pk=risk_profile_id)

            if risk_profile.exists():
                filter_dict['risk_profile'] = risk_profile
                risk_factor_id = body['risk_factor_id']
                risk_factor = RiskFactor.objects.filter(pk=risk_factor_id)

                if risk_factor.exists():
                    risk_factor_conditionals = self.model.objects.filter(**filter_dict).values()
                    return JsonResponse(dict(risk_conditionals=list(risk_factor_conditionals)))
                else:
                    return JsonResponse({'status': 'FAIL', 'message': 'Risk Factor does not exist.'})
            else:
                return JsonResponse({'status': 'FAIL', 'message': 'Risk Profile provided does not exist.'})
        else:
            return JsonResponse({'status': 'FAIL', 'message': 'Risk Profile ID must be provided.'})


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
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
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
                    cpr = high_yield_spread * -10/9 + 245/9
                    new_assumption_profile.constant_prepayment_rate = cpr
                if key == 'recovery':
                    recovery = national_home_price_index * 2.5 + 50
                    new_assumption_profile.recovery = recovery
                if key == 'lag':
                    lag = value
                    new_assumption_profile.lag = lag

        new_assumption_profile.save()
        return JsonResponse({'status': 'OK', 'message': 'Assumption Profile Created!!'})
