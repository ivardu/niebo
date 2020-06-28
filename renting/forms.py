from django import forms

class SearchForm(forms.Form):
	place = forms.CharField(widget=forms.TextInput(attrs={'class':'input' ,'placeholder':'Search place'}))