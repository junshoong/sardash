import os
import json
import errno
import subprocess
from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import Http404
from django.utils.dateformat import DateFormat

from sardash.settings import SA_ROOT

TODAY = DateFormat(datetime.now()).format('d')


def command_sar(ip, resource, date):
    try:
        if resource == 'cpu':
            option = '-u'
        elif resource == 'memory':
            option = '-r'
        elif resource == 'paging':
            option = '-B'
        else:
            option = ''

        command = os.popen("sar "+option+" -f "+SA_ROOT+ip+"/sa"+date)
        raw_data = command.read().strip().split('\n')
        data = raw_data[5:-1]
        row = []
        for x in data:
            row.append(x.split())

    except Exception as err:
        row = str(err)

    return row


def get_sar_data(request, ip='127.0.0.1', resource='cpu', date=TODAY):
    try:
        data = command_sar(ip, resource, date)
    except Exception:
        data = None
    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    response.write(data)

    return response


def get_remote_sar(ip):
    print('here is view', ip)
    try:
        full_path = SA_ROOT+ip
        print('mkdir', full_path)
        os.makedirs(full_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise 

    print('run scp')
    cp = subprocess.run(['scp', 'root@'+ip+':/var/log/sysstat/sa'+TODAY,full_path])
    if cp.returncode != 0:
        subprocess.run(['scp', 'root@'+ip+':/var/log/sa/sa'+TODAY,full_path])
    

def download(request, ip, file_name):
    file_path = os.path.join(SA_ROOT, ip, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'inline; filename='+ os.path.basename(file_path)
            return response
    raise Http404


def file_list(request, ip='127.0.0.1'):
    if ip:
        files = os.listdir(SA_ROOT+ip)
    else:
        files = os.listdir(SA_ROOT)
    return render_to_response('file_list.html', {'files': files})
