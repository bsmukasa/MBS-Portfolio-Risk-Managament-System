from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from portfolio.models import Portfolio


# Create your views here.
class PortfolioAPI(View):
    model = Portfolio

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PortfolioAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """ Gets all loan portfolios meeting filter values.

        Args:
            request: Request

        Returns:
             Json object with portfolios.
             Example:
                 {
                    portfolios: [
                        {
                            name: 'Portfolio Name',
                            date_created: '2015-05-03',
                            last_updated: '2015-09-21',
                            total_loan_balance: 100000000.0000,
                            total_loan_count: 5000,
                            average_loan_balance: 100000.0000,
                            weighted_average_coupon: 0.05463
                            weighted_average_life_to maturity: 354.2543
                        }
                    ]
                 }
        """
        # TODO Uncomment next two lines and filter_dict['user'] when user app is installed and working.
        filter_dict = request.GET.dict()
        portfolios = self.model.objects.filter(**filter_dict).values()

        return JsonResponse(dict(portfolios=list(portfolios)))
