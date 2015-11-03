from django.conf import settings
from django.db import models


# Create your models here.
class Portfolio(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_update = models.DateField(auto_now=True)
    total_loan_balance = models.IntegerField()
    total_loan_count = models.IntegerField()
    average_loan_balance = models.DecimalField(decimal_places=2, max_digits=20)
    weighted_average_coupon = models.DecimalField(decimal_places=5, max_digits=20)
    weighted_average_life_to_maturity = models.DecimalField(decimal_places=5, max_digits=20)


class Loan(models.Model):
    portfolio = models.ForeignKey(Portfolio)
    bank_loan_id = models.CharField(max_length=30, blank=True, null=True)
    property_type_code = models.CharField(max_length=3, blank=True, null=True)
    occupancy_code = models.CharField(max_length=1, blank=True, null=True)
    product_type = models.CharField(max_length=10, blank=True, null=True)
    purpose = models.CharField(max_length=1, blank=True, null=True)
    mortgage_type = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    reset_index = models.CharField(max_length=6, null=True, blank=True)
    pmi_insurance = models.CharField(max_length=128, blank=True, null=True)
    as_of_date = models.DateField(null=True,blank=True)
    first_payment_date = models.DateField(null=True,blank=True)
    original_date = models.DateField(null=True,blank=True)
    first_index_rate_adjustment_date = models.DateField(null=True,blank=True)
    fico = models.IntegerField(blank=True, null=True)
    lien_position = models.IntegerField(blank=True, null=True)
    interest_reset_interval = models.IntegerField(null=True, blank=True)
    negam_initial_minimum_payment_period = models.IntegerField(null=True, blank=True)
    negam_payment_reset_frequency = models.IntegerField(null=True, blank=True)
    recast_frequency = models.DecimalField(decimal_places=4, max_digits=20, blank=True, null=True)
    recast_cap = models.DecimalField(decimal_places=4, max_digits=20, blank=True, null=True)
    original_rate = models.DecimalField(decimal_places=4, max_digits=20, blank=True, null=True)
    original_amount = models.DecimalField(decimal_places=5, max_digits=30, blank=True, null=True)
    original_term = models.DecimalField(decimal_places=5, max_digits=30, blank=True, null=True)
    original_appraisal_amount = models.DecimalField(decimal_places=5, max_digits=30, blank=True, null=True)
    gross_margin = models.DecimalField(decimal_places=5, max_digits=20, blank=True, null=True)
    lcap = models.DecimalField(decimal_places=5, max_digits=20, blank=True, null=True)
    lfloor = models.DecimalField(decimal_places=5, max_digits=20, blank=True, null=True)
    icap = models.DecimalField(decimal_places=3, max_digits=20, blank=True, null=True)
    pcap = models.DecimalField(decimal_places=3, max_digits=20, blank=True, null=True)
    first_recast_or_next_recast = models.DecimalField(decimal_places=3, max_digits=20, blank=True, null=True)

    # TODO Snapshot fields to be in LoanSnapShot class when functionality is added.
    # loan = models.ForeignKey(Loan)
    SF = models.CharField(max_length=256)
    status = models.CharField(max_length=7)
    BK_flag = models.CharField(max_length=1, null=True)
    MSR = models.CharField(max_length=1, null=True)
    second_lien_piggyback_flag = models.CharField(max_length=1, blank=True, null=True)
    remaining_term = models.IntegerField(blank=True, null=True) 
    amortized_term = models.IntegerField(null=True)
    IO_term = models.IntegerField(null=True, blank=True)
    current_FICO_score = models.IntegerField(null=True, blank=True)
    junior_lien_balance = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    current_property_value = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    deferred_balance = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    current_principal_balance = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    current_interest_rate = models.DecimalField(decimal_places=5, max_digits=20, blank=True, null=True)
    senior_lien_balance = models.DecimalField(decimal_places=3, max_digits=20, blank=True, null=True)
    modification_date = models.DateField(null=True,blank=True)
    foreclosure_referral_date = models.DateField(null=True,blank=True)
    current_value_date = models.DateField(null=True,blank=True)
    last_payment_received = models.DateField(null=True,blank=True)
    senior_lien_balance_date = models.DateField(null=True,blank=True)
    junior_lien_balance_date = models.DateField(null=True,blank=True)
    
    


# class LoanAdjustedAssumptions(models.Model):
#     loan = models.ForeignKey(Loan)  # TODO Change to loan snapshot when functionality is added.
#     adjusted_cdr = models.DecimalField()
#     adjusted_cpr = models.DecimalField()
#     adjusted_recovery = models.DecimalField()
#     adjusted_lag = models.DecimalField()
