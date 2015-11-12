from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from risk_management.models import RiskProfile, RiskFactor, RiskConditional, AssumptionProfile, Scenario
from portfolio.models import Loan


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

        filter_dict = request.GET.dict()
        risk_profiles = self.model.objects.filter(**filter_dict).values()

        return JsonResponse(dict(risk_profiles=list(risk_profiles)))

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
        request_result = request.POST.dict()
        name = request_result['name']

        new_risk_profile = self.model(name=name)
        new_risk_profile.save()
        saved_risk_profile = self.model.objects.filter(pk=new_risk_profile.pk).values()

        return JsonResponse(
            dict(status="OK", message="Risk Profile created", new_risk_profile=list(saved_risk_profile)[0]))


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

        filter_dict = request.GET.dict()

        risk_profile_id = filter_dict['risk_profile_id']
        risk_profile = RiskProfile.objects.filter(pk=risk_profile_id)

        if risk_profile.exists():
            filter_dict['risk_profile'] = risk_profile

            risk_profile_risk_factors = self.model.objects.filter(**filter_dict).values()
            return JsonResponse(dict(risk_factors=list(risk_profile_risk_factors)))
        else:
            return JsonResponse({'status': 'FAIL', 'message': 'Risk Profile provided does not exist.'})

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
                "attribute": "FICO",
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
        form_dict = request.POST.dict()

        if 'risk_profile_id' in form_dict.keys():
            risk_profile_id = form_dict['risk_profile_id']
            risk_profile = RiskProfile.objects.filter(pk=risk_profile_id)

            if risk_profile.exists():
                new_risk_factor = self.model()
                new_risk_factor.risk_profile = RiskProfile.objects.get(pk=risk_profile_id)
                new_risk_factor.attribute = form_dict['attribute']
                new_risk_factor.changing_assumption = form_dict['changing_assumption'].upper()
                new_risk_factor.percentage_change = form_dict['percentage_change']
                new_risk_factor.save()

                if 'value' in form_dict.keys():
                    if form_dict['value2'] == '':
                        conditionals_list = [
                            {'conditional': form_dict['conditional'], 'value': form_dict['value']}
                        ]
                    else:
                        conditionals_list = [
                            {'conditional': form_dict['conditional'], 'value': form_dict['value']},
                            {'conditional': form_dict['conditional2'], 'value': form_dict['value2']}
                        ]
                else:
                    conditionals_list = [{'conditional': '==', 'value': form_dict['conditional']}]

                for item in conditionals_list:
                    new_risk_condtional = RiskConditional(risk_factor=new_risk_factor)
                    new_risk_condtional.conditional = item['conditional']
                    new_risk_condtional.value = item['value']
                    new_risk_condtional.save()

                return JsonResponse({'status': 'OK', 'message': 'Risk Factor added.'})
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


class RiskFactorAttributeChoicesAPI(View):
    model = Loan

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RiskFactorAttributeChoicesAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):  
        """ Get all choices related to an attribute.

        Example Result:
            { "related_choices": [] }

            { "related_choices": ["CA", "NY", "MI"] }

        :param request: Request
        return: JsonResponse list of assumption profiles.
        """
        selected_attribute = request.GET.dict()['attribute']

        attribute_with_choices = {
            'mortgage_type': 'MORTGAGE_TYPE_CHOICES',
            'property_type': 'PROPERTY_TYPE_CODE_CHOICES',
            'purpose': 'PURPOSE_CHOICES',
            'lien_position': 'LIEN_POSITION_CHOICES',
            'PMI': 'PMI_CHOICES',
            'state': 'STATE_CHOICES'
        }
        
        choices = []
        if selected_attribute in attribute_with_choices.keys():
            attr_value = attribute_with_choices[selected_attribute]
            choices = getattr(self.model, attr_value)

        return JsonResponse({"attribute_choices": choices})


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

        post_data = request.POST.dict()
        name = post_data['name']
        gdp_growth = post_data['gdp_growth']
        unemployment_rate = post_data['unemployment_rate']
        national_home_price_index = post_data['national_home_price_index_growth']
        high_yield_spread = post_data['high_yield_spread']

        new_assumption_profile = self.model(
            name=name,
            gdp_growth=gdp_growth,
            unemployment_rate=unemployment_rate,
            national_home_price_index_growth=national_home_price_index,
            high_yield_spread=high_yield_spread
        )

        default_assumptions = {
            "constant_default_rate": post_data['constant_default_rate'],
            "constant_prepayment_rate": post_data['constant_prepayment_rate'],
            "recovery": post_data['recovery'],
            "lag": post_data['lag']
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


class AssumptionNameAPI(View):
    model = AssumptionProfile

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AssumptionNameAPI, self).dispatch(request, *args, **kwargs)

    def get(self):
        """ Get all saved assumption profiles.

        Example Result:
            {
                "assumption_profiles": [
                    {
                        "name": "3 Month Timber Shortage",
                        "id": 1
                    },
                    {
                        "name": "GDP Growing at 3%",
                        "id": 2
                    }
                ]
            }

        return: JsonResponse list of assumption profiles on success, status and message if not.
        """
        assumption_names = self.model.objects.values_list("id", "name")

        print(assumption_names)
        
        return JsonResponse(dict(assumption_names=list(assumption_names)))


class ScenarioAPI(View):
    model = Scenario

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ScenarioAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Get all saved scenarios.
        Example Result:
            {
                "scenarios": [
                    {
                        "id": 1,
                        "name" = "US growing 5%",
                        "date_created": "2015-10-30T21:16:06.398Z",
                        "last_updated": "2015-10-30T21:16:06.398Z",
                        "assumption_profile_id": 1,
                        "score_card_profile_id": 3,
                        "risk_profiles": [1, 5, 7, 8, 9]
                    },
                ]
            }

        :param request: Request
        return: JsonResponse list of assumption profiles on success, status and message if not.
        """
        filter_dict = request.GET.dict()
        scenarios = self.model.objects.filter(**filter_dict).values()

        return JsonResponse(dict(scenarios=list(scenarios)))

    def post(self, request):
        """ Creates a new scenario and saves it to the database.

        Request must include:
        - assumptions_profile_id
        - risk_profile_id_list

        Example Request:
            {
                "assumptions_profile_id": 25,
                "risk_profile_id_list": [5, 27, 4, 17, 28]
            }

        :param request: Request
        :return: JsonResponse including a status and message.
        """    
        request_dict = request.POST.dict()
        assumption_profile_id = request_dict['assumption_profile_id']
        risk_profile_id_list = request_dict['risk_profile_id_list']

        new_scenario = self.model(assumption_profile_id=assumption_profile_id)

        for risk_profile_id in risk_profile_id_list:

            new_scenario.risk_profiles.add(RiskProfile.objects.get(pk=risk_profile_id))

        new_scenario.save()

        return JsonResponse(dict(status="OK", message="Scenario created"))


class SingleScenarioAPI(View):
    model = Scenario

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SingleScenarioAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Get one given requested scenario.

        Example Result:
            {
                "scenario": [
                    {
                        "id": 1,
                        "name" = "US growing 5%",
                        "date_created": "2015-10-30T21:16:06.398Z",
                        "last_updated": "2015-10-30T21:16:06.398Z",
                        "assumption_profile": 1,
                        "score_card_profile": 3,
                        "risk_profiles": 1
                    },
                ]
            }

        :param request: Request
        return: JsonResponse list with selected scenario, status and message if not.
        """
        filter_dict = request.GET.dict()
        scenario_id = filter_dict["id"]
        single_scenario = self.model.objects.filter(pk=scenario_id).values()

        return JsonResponse(dict(scenario=list(single_scenario)))
