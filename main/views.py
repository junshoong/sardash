import os
import json
import errno

from django.http import HttpResponse
from django.shortcuts import render

from main.forms import IPForm

# Create your views here.

def _get_sar_cpu(ip):
    try:
        if ip is None:
            command = os.popen("sar")
        else:
            command = os.popen("sar -f /tmp/"+ip+"/sa*")
        raw_data = command.read().strip().split('\n')
        data = dict()
        data['info']= raw_data[0]
        data['start'] = raw_data[2]
        data['header'] = raw_data[4]
        data['body'] = raw_data[5:-1]
        data['avg'] = raw_data[-1]

        row = []
        for x in data['body']:
            row.append(x.split())

    except Exception as err:
        data = str(err)

    return row


def _get_sar_mem(ip):
    try:
        if ip is None:
            command = os.popen("sar -r")
        else:
            command = os.popen("sar -r -f /tmp/"+ip+"/sa*")
        raw_data = command.read().strip().split('\n')
        data = dict()
        data['info']= raw_data[0]
        data['start'] = raw_data[2]
        data['header'] = raw_data[4]
        data['body'] = raw_data[5:-1]
        data['avg'] = raw_data[-1]

        row = []
        for x in data['body']:
            row.append(x.split())

    except Exception as err:
        data = str(err)

    return row

def get_sar_mem(request, ip=None):
    try:
        data = _get_sar_mem(ip)
    except Exception:
        data = None
    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    response.write(data)

    return response
    

def get_sar_cpu(request, ip=None):
    try:
        data = _get_sar_cpu(ip)
    except Exception:
        data = None
    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    response.write(data)

    return response

def _get_remote_sar(ip):
    try:
        full_path = '/tmp/'+ip
        os.makedirs(full_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise 

    subprocess.run(['scp', 'root@'+ip+':/var/log/sysstat/*',full_path])
    

def get_remote_sar(request):
    form = IPForm(request.POST or None)
    if form.is_valid():
        return redirect('home')
    return render(request, 'main.html', {'form': form})

