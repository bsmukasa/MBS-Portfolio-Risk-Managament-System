from django.conf.urls import patterns, url
from analytics import views

urlpatterns = patterns(
    '',

    url(
        regex=r'^analyze_portfolio$',
        view=views.CashFlowsAPI.as_view(),
        name='analyze_portfolio_api'
    ),
)
