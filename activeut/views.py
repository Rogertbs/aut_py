import os
import subprocess
import csv
import requests, time, threading

from datetime import date
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
        print(request.POST)
        print(request.FILES)
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

        print(jsonData)

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
                    time.sleep(int(timeMsg) * 60)
                    print(f"{lead} <<>> {jsonData[lead]['name']}")           
                    data = {
                        "number": jsonData[lead]['name'],
                        "options": {
                            "delay": 3000,
                            "presence": "composing"
                        },
                        "textMessage": {
                            "text": jsonData[lead]['msg']
                        }
                    }
                    try:
                        #print(f"Send Message Simulate!!!")
                        response = requests.get(URL, headers=HEADERS, param=data)
                        print(response.json())
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