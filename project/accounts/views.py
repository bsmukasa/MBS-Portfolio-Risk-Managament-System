from django.shortcuts import render
from django.views.generic import View


class Index(View):
	template = "accounts/index.html"

	def get(self, request):
		return render(request, self.template)


class Login(View):
	template = "accounts/login.html"

	def get(self, request):
		return render(request, self.template)


class Signup(View):
	template = "accounts/signup.html"

	def get(self, request):
		return render(request, self.template)
