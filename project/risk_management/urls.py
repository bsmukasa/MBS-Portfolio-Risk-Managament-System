from django.conf.urls import patterns, url
from risk_management import views

urlpatterns = patterns(
    '',

    url(
        regex=r'^create_assumption_profile$',
        view=views.AssumptionProfileAPI.as_view(),
        name='create_assumption_profile_api'
    ),

    url(
        regex=r'^get_assumption_profiles$',
        view=views.AssumptionProfileAPI.as_view(),
        name='get_assumption_profiles_api'
    ),

    url(
        regex=r'^get_risk_profiles$',
        view=views.RiskProfileAPI.as_view(),
        name='get_risk_profile_api'
    ),

    url(
        regex=r'^risk_factors$',
        view=views.RiskFactorAPI.as_view(),
        name='risk_factors_api'
    ),
)