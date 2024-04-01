import csv, json , ast
import requests, time, threading
from threading import Thread
from datetime import datetime
from django.core.cache import cache
from activeut.models import campaigns
from activeut.models import leads_in
from activeut.models import customers
from datetime import datetime
from django.utils import timezone

class customersController():
    "Class handle input customers"

    def __init__(self):
        print("Initiate Customers")
    
    def _setCustomerUser(self, user_session_id, request):

        customers_all = customers.objects.all()
        for customer in customers_all:
            users_id_list = ast.literal_eval(customer.users_id)
            for list_id in users_id_list:
                if user_session_id == list_id:
                    print(f"achei {user_session_id} in {users_id_list} Set session customer >> {customer.id}")
                    # set id customer in session user logged
                    request.session['customer_user'] = customer.id