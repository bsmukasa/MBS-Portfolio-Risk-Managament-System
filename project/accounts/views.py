from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class Index(View):
	template = "accounts/index.html"

	def get(self, request):
		return render(request, self.template)


class Login(View):
	template = "accounts/login.html"
	form = AuthenticationForm

	def get(self, request):
		return render(request, self.template, {'form': self.form})

	def post(self, request):
		login_form = self.form(data=request.POST)
		if login_form.is_valid():
			login_form.clean()
			login(request, login_form.user_cache)
			return redirect("portfolio:dashboard")

		else:
			return JsonResponse({"message": "FAIL"})


class Signup(View):
	template = "accounts/signup.html"
	form = UserCreationForm

	def get(self, request):
		return render(request, self.template, {'form': self.form})


	def post(self, request):
		signup_form = self.form(data=request.POST)
		signup_form.save()
		return redirect("portfolio:dashboard")


class Contact(View):
	pass


class Logout(View):

	def get(self, request):
		logout(request)
		return redirect("accounts:home")


