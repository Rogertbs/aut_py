import os
import subprocess
import csv, json
import requests, time, threading

from activeut.controllers.activeutController import activeUtController
from activeut.controllers.customersController import customersController
from activeut.controllers.campaignsController import campaignsController

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
def campaigns_create(request):
    
    if request.method == 'POST':
       campaigns = campaignsController()
       campaigns._createCampaing(request)

    return render(request, 'campaigns.html')

@login_required(login_url='login_user')
def campaigns_index(request):
    
    # if request.method == 'POST':
    #    campaigns = campaignsController()
    #    campaigns._createCampaing(request)

    return render(request, 'campaigns/campaigns_index.html')

@login_required(login_url='login_user')
def home(request):
    
    print(request.POST)
    
    processCsv = activeUtController()
    fetch_campaigns = processCsv._fetch_campaigns(request)
    print(fetch_campaigns)
    # result = {
    #     'fetch_campaigns': [[{'id': '1', 'campaigns_name': 'teste'}]]
    # }
    result = {
        'fetch_campaigns': [fetch_campaigns]
    }

    if request.method == 'POST':
        timeMsg = request.POST['timeMsg']
        msgOut = request.POST['messageInput']
        csv_file = request.FILES['csvFileInput']
        campaign_id = request.POST['campaignSelect']
         
        resultcsv = processCsv._processInput(msgOut, campaign_id, csv_file)
        result_msg = processCsv._sendMessages(timeMsg, resultcsv, campaign_id)
        print(result_msg)
        
        return render(request, 'home.html', result)
    else:
        return render(request, 'home.html', result)



def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            user_session_id = request.user.id
            customers = customersController()
            customers._setCustomerUser(user_session_id, request)

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