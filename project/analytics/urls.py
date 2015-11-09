from django.conf.urls import patterns, url
from analytics import views

urlpatterns = patterns(
    '',

    url(
        regex=r'^get_cash_flows$',
        view=views.CashFlowsAPI.as_view(),
        name='get_cash_flows_api'
    ),
)
