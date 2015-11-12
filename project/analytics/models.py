from django.db import models
from risk_management.models import Scenario
from portfolio.models import Portfolio


# Create your models here.
class CashFlowsResults(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    scenario = models.ForeignKey(Scenario)
    portfolio = models.ForeignKey(Portfolio)
    analysis_results_file_name = models.CharField()
