# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, abort, json, Response
from flask import session, g, redirect, url_for, abort, render_template, flash

import sys
import json
import logging
from logging.handlers import RotatingFileHandler

from flask.ext.socketio import SocketIO, emit

from functools import wraps

import xml.etree.ElementTree as ET

from ObmenMonitorDataService import ObmenLogItem, ObmenMonitorService, ObmenLogClient, ObmenCurrentErrorItem, ObmenCurrentStatusItem

from datetime import datetime
from time import strftime, gmtime

app = Flask(__name__)

import eventlet
eventlet.monkey_patch()

import time
from threading import Thread
thread = None

socketio = SocketIO(app, async_mode="eventlet")

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:

        count += 1
        obmenMonitorService = ObmenMonitorService()
        client_items = obmenMonitorService.getObmenClients()
        datajs = []
        for client_item in client_items:
            client_obmen_status = obmenMonitorService.getObmenStatusForClient(client_item['client_id'])
            datajs.append(dict(client=client_item, status_array=client_obmen_status))
            #datajs.append(dict(client=client_item))


        curTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        socketio.emit('my response',
                      {'data': curTime, 'count': count, 'clients': json.dumps(datajs)},
                      namespace='/test')
        time.sleep(5)

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
    # global thread
    # if thread is None:
    #     thread = Thread(target=background_thread)
    #     thread.daemon = True
    #     thread.start()
    # log_list=False
    #obmenMonitorService= ObmenMonitorService()
    #client_items = obmenMonitorService.getObmenClients()
    #return render_template(u'index.html', errors=errors, log_list=log_list, client_items=client_items)
    return render_template(u'landing.html')

@app.route("/monitor")
def monitor(errors=None):
    log_list=False
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    log_list=False
    obmenMonitorService= ObmenMonitorService()
    client_items = obmenMonitorService.getObmenClients()
    return render_template(u'index.html', errors=errors, log_list=log_list, client_items=client_items)
    #return render_template(u'landing.html')

@app.route("/log")
#@requires_auth
def log_items(errors=None):
    log_list=True
    obmenMonitorService= ObmenMonitorService()
    log_items = obmenMonitorService.getObmenLogItems()
    return render_template(u'show_log.html', log_items=log_items, log_list=log_list)

@app.route("/clients")
#@requires_auth
def client_items(errors=None):
    obmenMonitorService= ObmenMonitorService()
    client_items = obmenMonitorService.getObmenClients()
    return render_template(u'show_clients.html', client_items=client_items)

@app.route("/edit_client/<clientid>", methods=['GET', 'POST'])
def edit_client(clientid):
    obmenMonitorService = ObmenMonitorService()
    client = obmenMonitorService.getClientByID(clientid)
    uzels = obmenMonitorService.getUzelsForClient(clientid)
    if request.method == 'POST':
        client.client_name = request.form['name']
        client.client_id = request.form['clientid']
        #client.ib_key = request.form['ib_key']
        obmenMonitorService.updateClient(client)
        return redirect(url_for('client_items'))

    return render_template(u'edit_client.html', client=client, uzels=uzels)

@app.route("/delete_client/<clientid>", methods=['GET', 'POST'])
def delete_client(clientid):
    obmenMonitorService = ObmenMonitorService()
    client = obmenMonitorService.getClientByID(clientid)
    obmenMonitorService.deleteClient(client)
    return redirect(url_for('edit_client', clientid))

@app.route("/delete_uzel/<clientid>/<uzel>", methods=['GET', 'POST'])
def delete_uzel(clientid, uzel):
    obmenMonitorService = ObmenMonitorService()
    obmenMonitorService.deleteClientUzel(clientid, uzel)
    return redirect(url_for('client_items'))


@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username']=="kwl")&(request.form['password']=="123"):
            error = u''
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('monitor'))
        else:
            error=u'Не верный  логин или пароль'
            session['logged_in'] = False
            session['username'] = ''
            print(request.form.get('password',None))
            return render_template(u'login_form.html', errors=error)
    else:
        return render_template(u'login_form.html', errors=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', '')
    return redirect(url_for('hello'))


@app.route("/post_log", methods=['POST'])
@requires_auth
def post_log():
    obmenMonitorService= ObmenMonitorService()
    root = ET.fromstring(request.data)
    client_id = root.attrib['IDKlient']
    client = ObmenLogClient(client_id,'')
    client = obmenMonitorService.addClientItem(client)
    for child in root:
        # try:
        #     period = datetime.strptime(child.attrib['period'],'%d.%m.%Y %H:%M:%S')
        # except:
        #     period = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
        uzelib = child.attrib['uzelib']

        #Получим текущее состояние обмена и изменим его
        try:
            current_status = obmenMonitorService.getObmenCurrentStatus(client_id, uzelib)
        except:
            app.logger.error('Error on  getObmenCurrentStatus()' + sys.exc_info()[0])

        if current_status:
            pass
        else:
            current_status = ObmenCurrentStatusItem(client_id,uzelib)

        res_vigr = child.attrib['rezult_posl_vigr']
        res_zagr = child.attrib['rezult_posl_zagr']

        if res_vigr:
            current_status.Comment_vigruzka = child.attrib['comment_vigruzka']
            current_status.Rezult_posl_vigr = child.attrib['rezult_posl_vigr']
            try:
                current_status.Data_posl_vigr = datetime.strptime(child.attrib['data_posl_vigr'],'%d.%m.%Y %H:%M:%S')
            except:
                current_status.Data_posl_vigr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')

        if res_zagr:

            current_status.Comment_zagruzka = child.attrib['comment_zagruzka']
            current_status.Rezult_posl_zagr = child.attrib['rezult_posl_zagr']

            try:
                current_status.Data_posl_zagr = datetime.strptime(child.attrib['data_posl_zagr'],'%d.%m.%Y %H:%M:%S')
            except:
                current_status.Data_posl_zagr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')

        # try:
        #     li.Data_nachala_posl_vigr = datetime.strptime(child.attrib['data_nachala_posl_vigr'],'%d.%m.%Y %H:%M:%S')
        # except:
        #     li.Data_nachala_posl_vigr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
        # try:
        #     li.Data_nachala_posl_zagr = datetime.strptime(child.attrib['data_nachala_posl_zagr'],'%d.%m.%Y %H:%M:%S')
        # except:
        #     li.Data_nachala_posl_zagr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')

        #obmenMonitorService.addObmenLogItem(li)

        current_status.Last_exchange = datetime.now()
        try:
            obmenMonitorService.updateCurrentStatus(current_status)
        except:
            app.logger.error('Error on  updateCurrentStatus()' + sys.exc_info()[0])



    return render_template(u'show_log.html')

@app.route("/post_event", methods=['POST'])
#@requires_auth
def post_event():
    obmenMonitorService= ObmenMonitorService()
    root = request.data


    return render_template(u'show_log.html')

@app.route("/put_log", methods=['PUT'])
#@requires_auth
def put_log():
    #print(request.data)
    # obmenMonitorService= ObmenMonitorService()
    # root = ET.fromstring(request.data)
    # client_id = root.attrib['IDKlient']
    # client = ObmenLogClient(client_id,'')
    # client = obmenMonitorService.addClientItem(client)
    # for child in root:
    #     try:
    #         period = datetime.strptime(child.attrib['period'],'%d.%m.%Y %H:%M:%S')
    #     except:
    #         period = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
    #
    #     li = ObmenLogItem(client_id, period, child.attrib['uzelib'])
    #     li.Comment_vigruzka = child.attrib['comment_vigruzka']
    #     li.Comment_zagruzka = child.attrib['comment_zagruzka']
    #     li.Rezult_posl_vigr = child.attrib['rezult_posl_vigr']
    #     li.Rezult_posl_zagr = child.attrib['rezult_posl_zagr']
    #     try:
    #         li.Data_posl_zagr = datetime.strptime(child.attrib['data_posl_zagr'],'%d.%m.%Y %H:%M:%S')
    #     except:
    #         li.Data_posl_zagr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
    #     try:
    #         li.Data_posl_vigr = datetime.strptime(child.attrib['data_posl_vigr'],'%d.%m.%Y %H:%M:%S')
    #     except:
    #         li.Data_posl_vigr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
    #     try:
    #         li.Data_nachala_posl_vigr = datetime.strptime(child.attrib['data_nachala_posl_vigr'],'%d.%m.%Y %H:%M:%S')
    #     except:
    #         li.Data_nachala_posl_vigr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
    #     try:
    #         li.Data_nachala_posl_zagr = datetime.strptime(child.attrib['data_nachala_posl_zagr'],'%d.%m.%Y %H:%M:%S')
    #     except:
    #         li.Data_nachala_posl_zagr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')
    #
    #     obmenMonitorService.addObmenLogItem(li)
    #
    #     if (li.Rezult_posl_zagr == u"Нет"):
    #         li = ObmenLogItem(client_id, period, child.attrib['uzelib'])
    #         ei = ObmenCurrentErrorItem(client_id, period, li.uzelib)
    #         ei.Comment_vigruzka = li.Comment_vigruzka
    #         obmenMonitorService.addObmenErrorItem(ei)
    #         client.client_has_error = 1
    #         obmenMonitorService.updateClient(client)
    #         socketio.emit('my response',
    #                   {'data': 'Server put request'},
    #                   namespace='/test')
    #
    # return render_template(u'show_log.html')
    obmenMonitorService= ObmenMonitorService()
    root = ET.fromstring(request.data)
    client_id = root.attrib['IDKlient']
    client = ObmenLogClient(client_id,'')
    client = obmenMonitorService.addClientItem(client)
    for child in root:
        uzelib = child.attrib['uzelib']

        #Получим текущее состояние обмена и изменим его
        current_status = obmenMonitorService.getObmenCurrentStatus(client_id, uzelib)
        if current_status:
            pass
        else:
            current_status = ObmenCurrentStatusItem(client_id,uzelib)

        res_vigr = child.attrib['rezult_posl_vigr']
        res_zagr = child.attrib['rezult_posl_zagr']

        if res_vigr:
            current_status.Comment_vigruzka = child.attrib['comment_vigruzka']
            current_status.Rezult_posl_vigr = child.attrib['rezult_posl_vigr']
            try:
                current_status.Data_posl_vigr = datetime.strptime(child.attrib['data_posl_vigr'],'%d.%m.%Y %H:%M:%S')
            except:
                current_status.Data_posl_vigr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')

        if res_zagr:

            current_status.Comment_zagruzka = child.attrib['comment_zagruzka']
            current_status.Rezult_posl_zagr = child.attrib['rezult_posl_zagr']

            try:
                current_status.Data_posl_zagr = datetime.strptime(child.attrib['data_posl_zagr'],'%d.%m.%Y %H:%M:%S')
            except:
                current_status.Data_posl_zagr = datetime.strptime("01.01.0001 00:00:00",'%d.%m.%Y %H:%M:%S')

        current_status.Last_exchange = datetime.now()
        obmenMonitorService.updateCurrentStatus(current_status)

    return render_template(u'show_log.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})

if __name__ == "__main__":
   app.secret_key = 'sadkghsdkjfghadjghjksdgh'
   #app.run(host='localhost',port=8088, debug=False)

   handler = RotatingFileHandler('1Cmonitor.log', maxBytes=10000, backupCount=1)
   handler.setLevel(logging.INFO)
   app.logger.addHandler(handler)

   socketio.run(app, host='localhost', port=8088)
