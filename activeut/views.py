import os
import subprocess
import csv, json
import requests, time, threading

from activeut.controllers.activeutController import activeUtController

from datetime import datetime
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import FileResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Check if threads actives  
active_threads = []

@login_required(login_url='login_user')
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required(login_url='login_user')
def home(request):

    if request.method == 'POST':
        timeMsg = request.POST['timeMsg']
        msgOut = request.POST['messageInput']
        csv_file = request.FILES['csvFileInput']
        processCsv = activeUtController()
        resultcsv = processCsv._processInput(msgOut, csv_file)
        result_msg = processCsv._sendMessages(timeMsg, resultcsv)
        print(result_msg)
        
        return render(request, 'home.html', {"status": "true"})
    else:
        return render(request, 'home.html', {"status": "false"})



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