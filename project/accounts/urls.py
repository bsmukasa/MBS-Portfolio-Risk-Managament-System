from django.conf.urls import patterns, include, url
from django.contrib import admin
from front.views import Index, Login, Signup, Dashboard


urlpatterns = patterns(
	"",
	url(r'^$', Index.as_view(), name="home"),
	url(r'^login/$', Login.as_view(), name="login"),
	url(r'^signup/$', Signup.as_view(), name="signup"),
	url(r'^dashboard/$', Dashboard.as_view(), name="dashboard"),
	)