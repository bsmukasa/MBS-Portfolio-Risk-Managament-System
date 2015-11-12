from django.conf.urls import patterns, url
from risk_management import views

urlpatterns = patterns(
    '',

    url(
        regex=r'^assumption_profile$',
        view=views.AssumptionProfileAPI.as_view(),
        name='assumption_profile_api'
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
        regex=r'^risk_factor_conditionals$',
        view=views.RiskConditionalAPI.as_view(),
        name='risk_conditionals_api'
    ),

    url(
        regex=r'^score_card_profile$',
        view=views.ScoreCardProfileAPI.as_view(),
        name='score_card_profile_api'
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

    url(
        regex=r'^factor_attribute$',
        view=views.RiskFactorAttributeChoicesAPI.as_view(),
        name='risk_factor_api'
    ),

    url(
        regex=r'^scenarios$',
        view=views.ScenarioAPI.as_view(),
        name='scenario_api'
    ),

    url(
        regex=r'^assumptions_name$',
        view=views.AssumptionNameAPI.as_view(),
        name='assumptions_name_api'
    ),
)

