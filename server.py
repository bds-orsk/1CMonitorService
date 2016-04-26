# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, abort, json, Response
from flask import session, g, redirect, url_for, abort, render_template, flash

from functools import wraps

import xml.etree.ElementTree as ET

from ObmenMonitorDataService import ObmenLogItem, ObmenMonitorService

from datetime import datetime

app = Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'user' and password == '12345'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def hello(errors=None):
    log_list=False
    return render_template(u'index.html', errors=errors, log_list=log_list)

@app.route("/log")
#@requires_auth
def log_items(errors=None):
    log_list=True
    obmenMonitorService= ObmenMonitorService()
    log_items = obmenMonitorService.getObmenLogItems()
    return render_template(u'show_log.html', log_items=log_items, log_list=log_list)


@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username']=="kwl")&(request.form['password']=="123"):
            error = u''
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('hello'))
        else:
            error=u'Не верный  логин или пароль'
            session['logged_in'] = False
            session['username'] = ''
            print(request.form.get('password',None))
            return render_template(u'index.html', errors=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', '')
    return redirect(url_for('hello'))


@app.route("/post_log", methods=['POST'])
@requires_auth
def post_log():
    #print(request.data)
    obmenMonitorService= ObmenMonitorService()
    root = ET.fromstring(request.data)
    client_id = root.attrib['IDKlient']
    for child in root:
        try:
            period = datetime.strptime(child.attrib['period'],'%d.%m.%Y %H:%M:%S')
        except:
            period = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')

        li = ObmenLogItem(client_id, period, child.attrib['uzelib'])
        li.Comment_vigruzka = child.attrib['comment_vigruzka']
        li.Comment_zagruzka = child.attrib['comment_zagruzka']
        li.Rezult_posl_vigr = child.attrib['rezult_posl_vigr']
        li.Rezult_posl_zagr = child.attrib['rezult_posl_zagr']
        try:
            li.Data_posl_zagr = datetime.strptime(child.attrib['data_posl_zagr'],'%d.%m.%Y %H:%M:%S')
        except:
            li.Data_posl_zagr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
        try:
            li.Data_posl_vigr = datetime.strptime(child.attrib['data_posl_vigr'],'%d.%m.%Y %H:%M:%S')
        except:
            li.Data_posl_vigr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
        try:
            li.Data_nachala_posl_vigr = datetime.strptime(child.attrib['data_nachala_posl_vigr'],'%d.%m.%Y %H:%M:%S')
        except:
            li.Data_nachala_posl_vigr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
        try:
            li.Data_nachala_posl_zagr = datetime.strptime(child.attrib['data_nachala_posl_zagr'],'%d.%m.%Y %H:%M:%S')
        except:
            li.Data_nachala_posl_zagr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')

        obmenMonitorService.addObmenLogItem(li)
    return render_template(u'show_log.html')

@app.route("/put_log", methods=['PUT'])
@requires_auth
def put_log():
    #print(request.data)
    obmenMonitorService= ObmenMonitorService()
    root = ET.fromstring(request.data)
    client_id = root.attrib['IDKlient']
    for child in root:
        try:
            period = datetime.strptime(child.attrib['period'],'%d.%m.%Y %H:%M:%S')
        except:
            period = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')

        li = ObmenLogItem(client_id, period, child.attrib['uzelib'])
        li.Comment_vigruzka = child.attrib['comment_vigruzka']
        li.Comment_zagruzka = child.attrib['comment_zagruzka']
        li.Rezult_posl_vigr = child.attrib['rezult_posl_vigr']
        li.Rezult_posl_zagr = child.attrib['rezult_posl_zagr']
        try:
            li.Data_posl_zagr = datetime.strptime(child.attrib['data_posl_zagr'],'%d.%m.%Y %H:%M:%S')
        except:
            li.Data_posl_zagr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
        try:
            li.Data_posl_vigr = datetime.strptime(child.attrib['data_posl_vigr'],'%d.%m.%Y %H:%M:%S')
        except:
            li.Data_posl_vigr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
        try:
            li.Data_nachala_posl_vigr = datetime.strptime(child.attrib['data_nachala_posl_vigr'],'%d.%m.%Y %H:%M:%S')
        except:
            li.Data_nachala_posl_vigr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
        try:
            li.Data_nachala_posl_zagr = datetime.strptime(child.attrib['data_nachala_posl_zagr'],'%d.%m.%Y %H:%M:%S')
        except:
            li.Data_nachala_posl_zagr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')

        obmenMonitorService.addObmenLogItem(li)
    return render_template(u'show_log.html')


if __name__ == "__main__":
   app.secret_key = 'sadkghsdkjfghadjghjksdgh'
   app.run(host='localhost',port=8088, debug=False)
