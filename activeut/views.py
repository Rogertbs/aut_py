import os
import subprocess
import csv, json
import requests, time, threading

from activeut.controllers.activeutController import activeUtController
from activeut.controllers.customersController import customersController
from activeut.controllers.campaignsController import campaignsController
from activeut.controllers.messagesController import messagesController

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
def leads_index(request):

    processCsv = activeUtController()
    fetch_campaigns = processCsv._fetch_campaigns(request)
    result = {
        'fetch_campaigns': [fetch_campaigns]
    }
    
    if request.method == 'POST':
        fetch_leads = processCsv._fetch_leads(request)
        result = {
            'fetch_leads': [fetch_leads],
            'fetch_campaigns': [fetch_campaigns]
        }
        return render(request, 'leads/leads_index.html', result)
    
    return render(request, 'leads/leads_index.html', result)


@login_required(login_url='login_user')
def leads_in(request):
    
    #print(request.POST)
    
    processCsv = activeUtController()
    fetch_campaigns = processCsv._fetch_campaigns(request)
    # result = {
    #     'fetch_campaigns': [[{'id': '1', 'campaigns_name': 'teste'}]]
    # }
    result = {
        'fetch_campaigns': [fetch_campaigns]
    }

    if request.method == 'POST':
        csv_file = request.FILES['csvFileInput']
        campaign_id = request.POST['campaignSelect']
         
        resultcsv = processCsv._processInput(campaign_id, csv_file)
        
        #return render(request, 'campaigns/campaigns_index.html', result)
        return redirect('campaigns_index')
    else:
        return render(request, 'leads/leads_in.html', result)

@login_required(login_url='login_user')
def messages_create(request):

    result = None
    
    processCsv = activeUtController()
    fetch_campaigns = processCsv._fetch_campaigns(request)
    result = {
        'fetch_campaigns': [fetch_campaigns]
    }
    
    if request.method == 'POST':
        messages = messagesController()
        result = messages._createMessage(request)
    
    if result is True:
        processCsv = activeUtController()
        fetch_campaigns = processCsv._fetch_campaigns(request)
        result = {
            'fetch_campaigns': [fetch_campaigns]
        }

        return render(request, 'leads/leads_in.html', result)

    return render(request, 'messages/messages_create.html', result)


@login_required(login_url='login_user')
def messages_index(request):
    
    processCsv = activeUtController()
    fetch_messages = processCsv._fetch_messages(request)

    result = {
        'fetch_messages': [fetch_messages]
    }
    
    return render(request, 'messages/messages_index.html', result)


@login_required(login_url='login_user')
def campaigns_create(request):
    
    result = None

    processCsv = activeUtController()
    fetch_instances = processCsv._fetch_instances(request)
    result_instances = {
        'fetch_instances': [fetch_instances]
    }
    
    if request.method == 'POST':
       campaigns = campaignsController()
       result = campaigns._createCampaing(request)
    
    if result is True:
        processCsv = activeUtController()
        fetch_campaigns = processCsv._fetch_campaigns(request)

        result = {
            'fetch_campaigns': [fetch_campaigns]
        }
        return render(request, 'messages/messages_create.html', result)

    return render(request, 'campaigns/campaigns_create.html', result_instances)

@login_required(login_url='login_user')
def campaigns_index(request):
    
    processCsv = activeUtController()
    fetch_campaigns = processCsv._fetch_campaigns(request)
    #print(fetch_campaigns)

    result = {
        'fetch_campaigns': [fetch_campaigns]
    }
    #print(result)

    return render(request, 'campaigns/campaigns_index.html', result)

@login_required(login_url='login_user')
def handle_campaign(request):
    
    print(f"HANDLECAMPAING  >>> {request}")

    if request.method == 'POST':
        handleCampaign = activeUtController()
        result_msg = handleCampaign._sendMessages(request)
        #print(result_msg)
        return render(request, 'campaigns/campaigns_index.html')



@login_required(login_url='login_user')
def home(request):

    processCsv = activeUtController()
    fetch_campaigns = processCsv._fetch_campaigns(request)

    result = {
        'fetch_campaigns': [fetch_campaigns]
    }
    #print(result)

    return render(request, 'campaigns/campaigns_index.html', result)



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

            return redirect('campaigns_index')
        else:
            messages.error(request, ("Usuario ou senha incorretos!"))
            return redirect("login_user")
    else:
        return render(request, 'login.html', {})

@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')