from django import forms

class FileForm(forms.Form):
	name = forms.CharField(label='Portfolio Name', max_length=150)
	loan_file = forms.FileField(label='Upload CSV file')
