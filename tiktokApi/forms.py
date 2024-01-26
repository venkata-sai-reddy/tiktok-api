# forms.py
from django import forms

class YourModelForm(forms.Form):
    file_name = forms.FileField(label='CSV File')
    # csv_file = forms.FileField()
