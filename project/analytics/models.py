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


class ScoreCard(models.Model):
    ASSUMPTION_CHOICES = (
        ('CDR', 'Constant Default Rate'),
        ('CPR', 'Constant Prepayment Rate'),
        ('RECOVERY', 'Recovery')
    )

    assumption_type = models.CharField(max_length=64, choices=ASSUMPTION_CHOICES)
    # total_score = models.DecimalField(decimal_places=4, max_digits=10)
    # updated_total_score = models.DecimalField(decimal_places=4, max_digits=10)


class ScoreCardAttribute(models.Model):
    score_card = models.ForeignKey(ScoreCard)
    attribute = models.CharField(max_length=32)
    weight = models.DecimalField(decimal_places=4, max_digits=10)
    original_index = models.DecimalField(decimal_places=2, max_digits=5)
    original_score = models.DecimalField(decimal_places=4, max_digits=10)
    # index_change = models.DecimalField(decimal_places=2, max_digits=5)
    # updated_score = models.DecimalField(decimal_places=4, max_digits=10)
