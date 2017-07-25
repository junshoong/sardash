from django.forms import ModelForm
from main.models import Server

class IPForm(ModelForm):
    class Meta:
        model = Server
        fields = ['ip']
