import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from risk_management.models import RiskProfile, RiskFactor, RiskConditional


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
        return JsonResponse(dict(risk_profiles=list(risk_profiles)))

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
        pass  # TODO Finish this get method


class AssumptionProfileAPI(View):
    def dispatch(self, request, *args, **kwargs):
        return super(AssumptionProfileAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Get all saved assumption profiles.

        Example Result:
            {
                "assumption_profile_list": {
                    "assumption_profile": [
                        {
                            "assumption_profile_id": 2,
                            "name": "US Economy Growing and 3%",
                            "date_created": "2015-6-23",
                            "last_updated": "2015-10-18",
                            "gdp_growth": 3.2,
                            "unemployment_rate": 7.2,
                            "national_home_price_index": 8.7,
                            "high_yield_spread": 6.7,
                            "constant_default_rate": 5.3,
                            "constant_prepayment_rate": 12.2,
                            "recovery": 80,
                            "lag": 24
                        },
                        {
                            "assumption_profile_id": 8,
                            "name": "Nevada Housing Collapse",
                            "date_created": "2015-09-02",
                            "last_updated": "2015-09-02",
                            "gdp_growth": 1.3,
                            "unemployment_rate": 8.6,
                            "national_home_price_index": -2,
                            "high_yield_spread": 3.8,
                            "constant_default_rate": 10.8,
                            "constant_prepayment_rate": 6.2,
                            "recovery": 35,
                            "lag": 72
                        }
                    ]
                }
            }

        :param request: Request
        return: JsonResponse list of assumption profiles on success, status and message if not.
        """
        pass

    def post(self, request):
        """ Creates a new assumption profile and saves it to the database.

        Json in the Request must include:
        - name
        - gdp_growth
        - unemployment_rate
        - national_home_price_index

        Example Request:
            {
                "economic_assumptions": {
                    "name": "U.S. Economy Growing 3%",
                    "gdp_growth": 3.2,
                    "unemployment_rate": 8.5,
                    "national_home_price_index_growth": 3.7
                }
            }

        All Economic Assumptions are given equal weight in calculations.

        Formulas:
            - CDR = (GDP * -1 + 6.5) + (Unemployment * 1.2 - 5.5)
            - CPR = Yield Spread * -1.1111111111 + 27.2222222222222
            - Recovery = HPI * 2.5 + 50

        :param request: Request.
        :return: JsonResponse with status and message.
        """
        pass
