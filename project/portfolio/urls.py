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
        view=views.Dashboard.as_view(),
        name='dashboard'
    ),

)

