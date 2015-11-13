from django.forms import ModelForm
from risk_management.models import AssumptionProfile

class AssumptionForm(ModelForm):

    #This is throwing an error, so it's commented out
    # def __init__(self, *args, **kwargs):
    #     super(AssumptionForm, self).__init__(*args, **kwargs)
    #     self.fileds['name'].required = True
    #     self.fileds['gdp_growth'].required = True
    #     self.fileds['unemployment_rate'].required = True
    #     self.fileds['national_home_price_index_growth'].required = True
    #     self.fileds['high_yield_spread'].required = True
    #     self.fileds['lag'].required = True


    class Meta:
        model = AssumptionProfile
        exclude = ['date_created', 'last_updated']
        labels = {
            'name': 'Name',
            'gdp_growth': 'GDP Growth',
            'unemployment_rate': 'Unemployment Rate',
            'national_home_price_index_growth': 'National Home Price Index Growth',
            'high_yield_spread': 'High Yield Spread',
            'constant_default_rate': 'Constant Default Rate (CDR)',
            'constant_prepayment_rate': 'Constant Prepayment Rate (CPR)',
            'recovery_percentage': 'Recovery'
        }
