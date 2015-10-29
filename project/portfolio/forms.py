from django import forms

class FileForm(forms.Form):
	portfolio_name = forms.CharField(label='Portfolio Name', max_length=150)
	docfile = forms.FileField(label='Upload CSV file')
