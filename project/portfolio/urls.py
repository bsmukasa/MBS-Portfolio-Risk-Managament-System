from django.conf.urls import patterns, url
from portfolio import views

urlpatterns = patterns(
    '',

    url(
        regex=r'^get_portfolios$',
        view=views.PortfolioAPI.as_view(),
        name='get_portfolios_api'
    ),

    url(
        regex=r'^dashboard$',
        view=views.DashboardView.as_view(),
        name='dashboard'
    ),

    url(
        regex=r'^sp/(?P<portfolio_id>.*)$',
        view=views.PortfolioView.as_view(),
        name='portfolio'
    ),

    url(
        regex=r'^all_loans$',
        view=views.LoanPaginationAPI.as_view(),
        name='all_loans_api'
    ),

    url(
        regex=r'^port_loans_status$',
        view=views.PortfolioStatusAPI.as_view(),
        name='portfolio_loans_status_api'
    ),

    url(
        regex=r'^fico_summary$',
        view=views.PortfolioFICOAPI.as_view(),
        name='fico_summary_api'
    ),
)
