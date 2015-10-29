import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from risk_management.models import RiskProfile, RiskFactor


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
    moodel = RiskFactor

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RiskFactorAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        pass

    def post(self, request):
        pass
