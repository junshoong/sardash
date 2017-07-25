from django.forms import ModelForm
from main.models import Server
from main import views as main

class IPForm(ModelForm):
    class Meta:
        model = Server
        fields = ['ip']

    def get_remote_sar_data(self, ip):
        print('here is form', ip)
        main.get_remote_sar(ip)
    
