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

        regex=r'^create_risk_profile$',
        view=views.RiskProfileAPI.as_view(),
        name='create_risk_profile_api'
    ),

    url(
        regex=r'^get_risk_profiles$',
        view=views.RiskProfileAPI.as_view(),
        name='get_risk_profiles_api'
    ),

    url(
        regex=r'^add_risk_factor$',
        view=views.RiskFactorAPI.as_view(),
        name='add_risk_factor_api'
    ),

    url(
        regex=r'^get_risk_factors$',
        view=views.RiskFactorAPI.as_view(),
        name='get_risk_factors_api'
    ),

    url(
        regex=r'^get_risk_factor_conditionals$',
        view=views.RiskConditionalAPI.as_view(),
        name='get_risk_conditionals_api'
    ),

    url(
        regex=r'^add_score_card_profile$',
        view=views.ScoreCardProfileAPI.as_view(),
        name='add_score_card_profile_api'
    ),

    url(
        regex=r'^get_score_card_profiles$',
        view=views.ScoreCardProfileAPI.as_view(),
        name='get_score_card_profiles_api'
    ),

    url(
        regex=r'^get_score_cards$',
        view=views.ScoreCardAPI.as_view(),
        name='get_score_cards_api'
    ),

    url(
        regex=r'^get_score_card_attributes$',
        view=views.ScoreCardAttributeAPI.as_view(),
        name='get_score_card_attributes_api'
    ),
)

