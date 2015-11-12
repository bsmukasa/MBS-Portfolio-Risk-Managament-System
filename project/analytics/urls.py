from django.conf.urls import patterns, url
from analytics import views

urlpatterns = patterns(
    '',

    url(
        regex=r'^analyze_portfolio$',
        view=views.CashFlowsAPI.as_view(),
        name='analyze_portfolio_api'
    ),

    url(
        regex=r'^get_aggregate_cash_flows$',
        view=views.AggregateCashFlowsAPI.as_view(),
        name='get_aggregate_cash_flows_api'
    ),
)
