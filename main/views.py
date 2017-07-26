import os
import json
import errno
import subprocess
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.dateformat import DateFormat

from main.forms import IPForm

TODAY = DateFormat(datetime.now()).format('d')


def _get_sar_cpu(ip):
    try:
        if ip is None:
            command = os.popen("sar")
        else:
            command = os.popen("sar -f /tmp/"+ip+"/sa"+TODAY)
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
            command = os.popen("sar -r -f /tmp/"+ip+"/sa"+TODAY)
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


def get_remote_sar(ip):
    print('here is view', ip)
    try:
        full_path = '/tmp/'+ip
        print('mkdir', full_path)
        os.makedirs(full_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise 

    print('run scp')
    subprocess.run(['scp', 'root@'+ip+':/var/log/sysstat/sa'+TODAY,full_path])
    
