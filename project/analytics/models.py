from django.db import models
from risk_management.models import Scenario
from portfolio.models import Portfolio


# Create your models here.
class CashFlowsResults(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    scenario = models.ForeignKey(Scenario)
    portfolio = models.ForeignKey(Portfolio)
    discount_rate = models.DecimalField(max_digits=10, decimal_places=4)
    analysis_results_name = models.CharField()
