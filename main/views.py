import os
import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def _get_sar_cpu():
    try:
        command = os.popen("sar")
        raw_data = command.read().strip().split('\n')
        data = dict()
        data['info']= raw_data[0]
        data['start'] = raw_data[2]
        data['header'] = raw_data[4]
        data['body'] = raw_data[5:-1]
        data['avg'] = raw_data[-1]

    except Exception as err:
        data = str(err)

    print(data)
    return data
    

def get_sar_cpu(request):
    try:
        data = _get_sar_cpu()
    except Exception:
        data = None
    data = json.dumps(data['body'])
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    response.write(data)

    return response
