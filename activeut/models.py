from django.db import models

"""
Create Class Model
Create migration make
python3 manage.py makemigrations activeut --empty (to create new migrate empty)
python3 manage.py migrate activeut

show sql migrate
python3 manage.py sqlmigrate activeut 0002_lead.py

show migrations
python3 manage.py showmigrations

how rollback a migration
python manage.py migrate your_app_name <migration_name_or_ID> --backward
"""

# Create model table campaigns
class campaigns(models.Model):
    id = models.AutoField(primary_key=True)
    campaigns_name = models.CharField(max_length=50)
    campaigns_describre = models.CharField(max_length=100)
    enabled = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.IntegerField(null=True)
    
# Create model table campaigns
class leads_in(models.Model):
    id = models.AutoField(primary_key=True)
    lead_name = models.CharField(max_length=50, null=False)
    lead_number = models.CharField(max_length=100, null=False)
    id_campaign = models.IntegerField(null=True)
    send_status = models.CharField(max_length=100)
    send_timestamp = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Create model table campaigns
class instances(models.Model):
    id = models.AutoField(primary_key=True)
    instance_name = models.CharField(max_length=100, null=False)
    api_key = models.CharField(max_length=255, null=False)
    url = models.CharField(max_length=255, null=False)
    id_user = models.IntegerField(null=True)
    id_customer = models.IntegerField(null=True)
    enabled = models.IntegerField(null=True)
    limit = models.IntegerField(null=True)
    contract_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Create model table customers
class customers(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100, null=False)
    cpf = models.BigIntegerField(null=True)
    cnpj = models.BigIntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    number_address = models.IntegerField(null=True)
    zip_code = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    contract_id = models.IntegerField(null=True)
    enabled = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    users_id = models.CharField(max_length=255, null=True)

# Create model table contracts plans
class contracts(models.Model):
    id = models.AutoField(primary_key=True)
    contract_name = models.CharField(max_length=150, null=False)
    contract_value = models.DecimalField(max_digits=10, decimal_places=2)
    limit = models.IntegerField(null=True)
    enabled = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Create model table bill_customers
class bill_customers(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField(null=True)
    contract_id = models.IntegerField(null=True)
    count_total = models.BigIntegerField(null=True)
    value_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

# Create model table messages campaigns
class messagens_campaigns(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField(null=True)
    campaign_id = models.IntegerField(null=True)
    instance_id = models.IntegerField(null=True)
    message = models.CharField(max_length=255, null=True)
    message_description = models.CharField(max_length=200, null=True)
    media_url = models.CharField(max_length=255, null=True)
    media_type = models.CharField(max_length=50, null=True)
    media_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    time_msg = models.IntegerField(null=True)


# Todo update created_at in customers auto now add...