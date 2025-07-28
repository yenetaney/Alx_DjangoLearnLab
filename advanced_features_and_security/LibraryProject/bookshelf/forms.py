from django import forms

class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=True)

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=100)
    author = forms.CharField(max_length=100)
    published_date = forms.DateField(widget=forms.SelectDateWidget)