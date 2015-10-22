from django.conf import settings
from django.db import models


# Create your models here.
class Loan(models.Model):
    portfolio = models.ForeignKey(Portfolio)
    as_of_date = models.DateField()
    property_type_code = models.CharField(max_length=3, choices=PROPERTY_TYPE_CODE_CHOICES)
    occupancy_code = models.CharField(max_length=1, choices=OWNER_OCCUPANCY_CODE_CHOICES)
    product_type = models.CharField()
    purpose = models.CharField()
    mortgage_type = models.CharField()
    lien_position = models.CharField()
    original_rate = models.CharField()
    first_payment_date = models.DateField()
    original_amount = models.DecimalField()
    original_term = models.IntegerField()
    pmi = models.DecimalField()
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    fico = models.IntegerField()
    gross_margin = models.DecimalField()
    lcap = models.DecimalField()
    lfloor = models.DecimalField()
    icap = models.DecimalField()
    pcap = models.DecimalField()
    interest_reset_interval = models.DecimalField()
    reset_index = models.DecimalField()
    first_index_rate_adjustment_date = models.DateField()
    first_recast_or_next_recast = models.CharField()
    recast_frequency = models.CharField()
    negam_initial_minimum_payment_period = models.IntegerField()
    negam_payment_reset_frequency = models.DecimalField()


class LoanSnapShot(models.Model):
    pass


class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_created=True)
