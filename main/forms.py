from django import forms

class IPForm(forms.Form):
    address = forms.GenericIPAddressField(protocol='IPv4')
