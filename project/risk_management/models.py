from django.db import models


# Create your models here.
class RiskProfile(models.Model):
    name = models.CharField(max_length=128)
    date_created = models.DateField(auto_now_add=True)


class RiskFactor(models.Model):
    pass


class AssumptionProfile(models.Model):
    pass


class ScoreCard(models.Model):
    pass


class ScoreCardAttribute(models.Model):
    pass


class ScoreCardAdjustments(models.Model):
    pass


class Scenario(models.Model):
    pass

