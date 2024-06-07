import os
import subprocess
import csv, json
import requests, time, threading

from activeut.controllers.activeutController import activeUtController
from activeut.controllers.customersController import customersController
from activeut.controllers.campaignsController import campaignsController
from activeut.controllers.messagesController import messagesController
from activeut.controllers.dashboardsController import dashboardsController
from activeut.controllers.instanceController import instanceController
from activeut.controllers.leadsController import leadsController

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

    lead = leadsController()
    camp = campaignsController()
    fetch_campaigns = camp._fetch_campaigns(request)
    result = {
        'fetch_campaigns': [fetch_campaigns]
    }
    
    if request.method == 'POST':
        fetch_leads = lead._fetch_leads(request)
        result = {
            'fetch_leads': [fetch_leads],
            'fetch_campaigns': [fetch_campaigns]
        }
        return render(request, 'leads/leads_index.html', result)
    
    return render(request, 'leads/leads_index.html', result)


@login_required(login_url='login_user')
def leads_in(request):
       
    camp = campaignsController()
    fetch_campaigns = camp._fetch_campaigns(request)

    result = {
        'fetch_campaigns': [fetch_campaigns]
    }

    if request.method == 'POST':
        csv_file = request.FILES['csvFileInput']
        campaign_id = request.POST['campaignSelect']
        
        processCsv = activeUtController()
        resultcsv = processCsv._processInput(campaign_id, csv_file)
        
        return redirect('campaigns_index')
    else:
        return render(request, 'leads/leads_in.html', result)

@login_required(login_url='login_user')
def messages_create(request):

    result = None
    
    camp = campaignsController()
    fetch_campaigns = camp._fetch_campaigns(request)
    result = {
        'fetch_campaigns': [fetch_campaigns]
    }
    
    if request.method == 'POST':
        messages = messagesController()
        result = messages._createMessage(request)
    
    if result is True:
        camp = campaignsController()
        fetch_campaigns = camp._fetch_campaigns(request)
        result = {
            'fetch_campaigns': [fetch_campaigns]
        }

        return render(request, 'leads/leads_in.html', result)

    return render(request, 'messages/messages_create.html', result)

@login_required(login_url='login_user')
def messages_update(request, id=None):

    if request.method == 'POST':
        
        id = request.POST['id_message']
        print(f"ID >> {id}")
        messages = messagesController()
        update_msg = messages._message_update(request, id) 
        if update_msg:
            fetch_messages = messages._fetch_messages(request)
            result = {
                'fetch_messages': [fetch_messages]
            }  
            return render(request, 'messages/messages_index.html', result)
        else:
            fetch_message = messages._fetch_messages(request, id)
            result = {
            'fetch_message': [fetch_message]
            }
            return render(request, 'messages/messages_update.html', result)     
    else:
        # Fetch campaigns
        camp = campaignsController()
        fetch_campaigns = camp._fetch_campaigns(request)
        messages = messagesController()
        fetch_message = messages._fetch_messages(request, id)
        result = {
        'fetch_message': [fetch_message],
        'fetch_campaigns': [fetch_campaigns]
        }
        print(result)
        return render(request, 'messages/messages_update.html', result)




@login_required(login_url='login_user')
def messages_index(request):
    
    messages = messagesController()
    fetch_messages = messages._fetch_messages(request)

    result = {
        'fetch_messages': [fetch_messages]
    }
    
    return render(request, 'messages/messages_index.html', result)


@login_required(login_url='login_user')
def campaigns_create(request):
    
    result = None
    instance = instanceController()
    fetch_instances = instance._fetch_instances(request)
    result_instances = {
        'fetch_instances': [fetch_instances]
    }
    
    if request.method == 'POST':
       campaigns = campaignsController()
       result = campaigns._createCampaing(request)
    
    if result is True:
        camp = campaignsController()
        fetch_campaigns = camp._fetch_campaigns(request)

        result = {
            'fetch_campaigns': [fetch_campaigns]
        }
        return render(request, 'messages/messages_create.html', result)

    return render(request, 'campaigns/campaigns_create.html', result_instances)

@login_required(login_url='login_user')
def campaigns_index(request):
    
    camp = campaignsController()
    fetch_campaigns = camp._fetch_campaigns(request)

    result = {
        'fetch_campaigns': [fetch_campaigns]
    }

    return render(request, 'campaigns/campaigns_index.html', result)


@login_required(login_url='login_user')
def campaigns_update(request, id=None):

    if request.method == 'POST':

        camp = campaignsController()
        update_camp = camp._campaign_update(request, id) 
        if update_camp:
            fetch_campaigns = camp._fetch_campaigns(request)
            result = {
                'fetch_campaigns': [fetch_campaigns]
            }  
            return render(request, 'campaigns/campaigns_index.html', result)
        else:
            fetch_campaigns = camp._fetch_campaigns(request, id)
            result = {
            'fetch_campaigns': [fetch_campaigns]
            }
            return render(request, 'campaigns/campaigns_update.html', result)     
    else:
        instance = instanceController()
        fetch_instances = instance._fetch_instances(request)
        # Fetch campaigns
        camp = campaignsController()
        fetch_campaigns = camp._fetch_campaigns(request, id)
        result = {
        'fetch_instances': [fetch_instances],
        'fetch_campaigns': [fetch_campaigns]
        }
        
        return render(request, 'campaigns/campaigns_update.html', result)


@login_required(login_url='login_user')
def handle_campaign(request):
    
    print(f"HANDLECAMPAING  >>> {request}")

    if request.method == 'POST':
        handleCampaign = activeUtController()
        result_msg = handleCampaign._sendMessages(request)
        #print(result_msg)
        return render(request, 'campaigns/campaigns_index.html')


@login_required(login_url='login_user')
def dashboard_campaigns(request):

    camp = campaignsController()
    fetch_campaigns = camp._fetch_campaigns(request)
    
    dash_statistics = dashboardsController()
    # fetch_total_delivered = dash_statistics._getTotalDeliverd(request)
    # print(f"Total Delivered >>>> {fetch_total_delivered}")
    
    # fetch_total_sent = dash_statistics._getTotalSent(request)
    # print(f"Total Sent >>>> {fetch_total_sent}")
    
    # fetch_total_false = dash_statistics._getTotalFalse(request)
    # print(f"Total False >>>> {fetch_total_false}")
    
    # fetch_total_active = dash_statistics._getTotalActive(request)
    # print(f"Total Active >>>> {fetch_total_active}")
    
    # fetch_total_outstanding = dash_statistics._getTotalOutstanding(request)
    # print(f"Total OutStanding >>>> {fetch_total_outstanding} \n")

    # fetch_details = dash_statistics._getDetails(request)
    # print(f"Total Details >>>> {fetch_details}")

    # result = {
    #     'fetch_campaigns': [fetch_campaigns],
    #     'fetch_total_delivered': [fetch_total_delivered],
    #     'fetch_total_sent': [fetch_total_sent],
    #     'fetch_total_false': [fetch_total_false],
    #     'fetch_total_active': [fetch_total_active],
    #     'fetch_total_outstanding': [fetch_total_outstanding],
    #     'fetch_details': [fetch_details]
    # }

    dash = dash_statistics._getDashboard(request)
    print(dash)

    result = {
        'fetch_campaigns': [fetch_campaigns],
        'fetch_total_delivered': [dash["total_delivered"]],
        'fetch_total_sent': [dash["total_sent"]],
        'fetch_total_false': [dash["total_false"]],
        'fetch_total_active': [dash["total_actives"]],
        'fetch_total_outstanding': [dash["outstanding"]],
        'fetch_details': [dash["details"]]
    }
    

    return render(request, 'dashboards/dashboard_campaigns.html', result)

#@login_required(login_url='login_user')
def dashboards_statistics(request):
      
    dash_statistics = dashboardsController()
    dash = dash_statistics._getDashboard(request)

    result = {
        'fetch_total_delivered': [dash["total_delivered"]],
        'fetch_total_sent': [dash["total_sent"]],
        'fetch_total_false': [dash["total_false"]],
        'fetch_total_active': [dash["total_actives"]],
        'fetch_total_outstanding': [dash["outstanding"]],
        'fetch_details': [dash["details"]]
    }

    from django.http import JsonResponse
    return JsonResponse(result)

@login_required(login_url='login_user')
def home(request):

    camp = campaignsController()
    fetch_campaigns = camp._fetch_campaigns(request)

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