from django.conf.urls import patterns, include, url
from django.contrib import admin
from accounts.views import Index, Login, Signup, Contact, Logout

urlpatterns = patterns(
	"",
	url(r'^$', Index.as_view(), name="home"),
	url(r'^login/$', Login.as_view(), name="login"),
	url(r'^signup/$', Signup.as_view(), name="signup"),
	url(r'^contact/$', Contact.as_view(), name="contact"),
	url(r'^logout/$', Logout.as_view(), name="logout"),

	)

