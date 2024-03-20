import os
import subprocess
import csv, json
import requests, time, threading

from datetime import datetime
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import FileResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout




@login_required(login_url='login_user')
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required(login_url='login_user')
def home(request):
    

    if request.method == 'POST':
        timeMsg = request.POST['timeMsg']
        msgOut = request.POST['messageInput']
        csv_file = request.FILES['csvFileInput']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        jsonData = {}
        i = 0
        for row in reader:
            tmp = row[0].split(";")
            jsonData[i] = { 
                'id': tmp[0],
                'name': tmp[1],
                'number': tmp[2],
                'msg': msgOut.replace("{name}", str(tmp[1]))
            }
            i = i+1

        URL = 'http://app.unifytalk.com.br:8080/message/sendText/evounifytalk'
        HEADERS = {
                'apikey': 'B6D711FCDE4D4FD5936544120E713976',
                'Content-Type': 'application/json'
              }
        
        def sendMessages(**kwargs):
            jsonData = kwargs['jsonData']
            timeMsg = kwargs['timeMsg']

            try:
                for lead in jsonData:
                    print(f"{lead} <<>> {jsonData[lead]['name']} >><< timestamp {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}")           
                    data = {
                        "number": jsonData[lead]['number'],
                        "options": {
                            "delay": 3000,
                            "presence": "composing"
                        },
                        "textMessage": {
                            "text": jsonData[lead]['msg']
                        }
                    }
                    
                    try:
                        response = requests.post(URL, headers=HEADERS, data=json.dumps(data))
                        print(response.json())
                        time.sleep(int(timeMsg) * 60)
                    except Exception as e:
                        print("_httpexecute returned Unknown Error: {}".format(str(e)))
                        return None
            except Exception as e:
                    print("_httpexecute returned Unknown Error: {}".format(str(e)))
                    return None
                

        
        #exec_thread = threading.Thread(target=sendMessages(jsonData, timeMsg)).start()
        threading.Thread(target=sendMessages, kwargs={'jsonData' : jsonData, 'timeMsg': timeMsg}).start()
        print("ok")


    return render(request, 'home.html', {"status": "true"})



def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, ("Usuario ou senha incorretos!"))
            return redirect("login_user")
    else:
        return render(request, 'login.html', {})

@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')