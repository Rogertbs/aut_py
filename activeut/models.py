from django.db import models

"""
Create Class Model
Create migration make
python3 manage.py makemigrations activeut
python3 manage.py migrate activeut

show sql migrate
python3 manage.py sqlmigrate activeut 0002_lead.py
"""

# Create model table campaigns
class campaigns(models.Model):
    id = models.AutoField(primary_key=True)
    campaigns_name = models.CharField(max_length=50)
    campaigns_describre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
# Create model table campaigns
class leads_in(models.Model):
    id = models.AutoField(primary_key=True)
    lead_name = models.CharField(max_length=50, null=False)
    lead_number = models.CharField(max_length=100, null=False)
    id_campaign = models.IntegerField(null=True)
    send_status = models.CharField(max_length=100)
    send_timestamp = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)