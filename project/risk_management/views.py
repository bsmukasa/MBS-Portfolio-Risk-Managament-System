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
        filter_dict = request.GET.dict()
        risk_profiles = self.model.objects.filter(**filter_dict).values()
        return JsonResponse(dict(risk_profiles=list(risk_profiles)))

    def post(self, request):
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
        """ Creates a new risk factor and related conditionals.

        Json in the Request must include:
        - risk_profile_id
        - risk_factor_attribute
        - changing_assumption
        - percentage_change
        - conditionals_list

        Example:
            {
                "risk_factor": {
                    "risk_profile_id": 5,
                    "risk_factor_attribute": "FICO",
                    "changing_assumption": "CDR",
                    "percentage_change": "-5",
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
