import csv, json
import requests, time, threading
from threading import Thread
from datetime import datetime
from activeut.models import messagens_campaigns
from datetime import datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from activeut.models import campaigns
from django.shortcuts import get_object_or_404
from django.db import connection


class messagesController(Thread):
    "Class handle input campaigns"

    def __init__(self):
        print("Initiate Campaigns")
        """_summary_
| id                  | int(11)      | NO   | PRI | NULL    | auto_increment |
| customer_id         | int(11)      | YES  |     | NULL    |                |
| campaign_id         | int(11)      | YES  |     | NULL    |                |
| instance_id         | int(11)      | YES  |     | NULL    |                |
| message             | varchar(255) | YES  |     | NULL    |                |
| message_description | varchar(200) | YES  |     | NULL    |                |
| media_url           | varchar(255) | YES  |     | NULL    |                |
| media_type          | varchar(50)  | YES  |     | NULL    |                |
| media_name          | varchar(255) | YES  |     | NULL    |                |
| created_at  
        """
    
    def _createMessage(self, request):
        try:
            #import pdb; pdb.set_trace()
            print(f"DEBUG: {request.POST}")
            campaign_id = request.POST['campaignSelect']
            message_description = request.POST['messageDescription']
            message = str(request.POST['messageInput'])
            time_msg = request.POST['timeMsg']
            created_at = self._convertStamp()
            customer_id = request.session.get('customer_main')
            #media_type = 'media' if request.POST.get('RadioMedia') else 'text'
            if 'RadioMedia' in request.POST.keys():
                media_type = 'media'
            else:
                media_type = 'text'

            if len(request.FILES) != 0:
                media_name = request.FILES['media']
            else:
                media_name = ''

            #media_name = request.FILES['media'] if request.get('FILES') else ''
            media_url = 'https://200.152.191.137/media/'

            fetch_instance_id = campaigns.objects.filter(id=campaign_id)
            for x in fetch_instance_id:
                instance_id = x.instance_id

            # Create an instance of YourModel
            new_message = messagens_campaigns(campaign_id=campaign_id,
                                        instance_id=instance_id,
                                        message_description=message_description,
                                        message=message,
                                        time_msg=time_msg,
                                        created_at=created_at,
                                        customer_id=customer_id[0],
                                        media_type=media_type,
                                        media_name=media_name,
                                        media_url=media_url)

            # Save the instance to the database
            result = new_message.save()
            print(result)
            
            if len(request.FILES) != 0:
                uploaded_file = request.FILES['media']
                fs = FileSystemStorage(location='/var/www/media/')  # Change this to your desired directory
                filename = fs.save(uploaded_file.name, uploaded_file)
                print(filename)
        except Exception as e:
            print(e)
            return False
        return True


    def _message_update(self, request, id=None):
        try:
            print(f"DEBUG POST: {request.POST}")
            print(f"DEBUG FILES: {request.FILES}")
            if request.POST['campaignSelect']:
                campaign_id = request.POST['campaignSelect']
            else:
                campaign_id = request.POST['campaign_id']
                message_description = request.POST['messageDescription']
                message = str(request.POST['messageInput'])
                time_msg = request.POST['timeMsg']
                created_at = self._convertStamp()
                customer_id = request.session.get('customer_main')
            if 'messageType' in request.POST.keys():
                media_type = 'media'
            else:
                media_type = 'text'
            
            if len(request.FILES) != 0:
                print(f"DEBUG FILES: {request.FILES['media']}")
                media_name = request.FILES['media']
                fs = FileSystemStorage(location='/var/www/media')
                filename = fs.save(media_name.name, media_name)
                file_url = fs.url(filename)
                print("Arquivo salvo em:", file_url)
            else:
                media_name = ''

            #media_name = request.FILES['media'] if request.get('FILES') else ''
            media_url = 'http://5.189.153.168:81/media/'

            fetch_instance_id = campaigns.objects.filter(id=campaign_id)
            for x in fetch_instance_id:
                instance_id = x.instance_id

            # Retrieve the item with ID 1
            msg_cp = get_object_or_404(messagens_campaigns, id=id)
            # Update the fields
            msg_cp.instance_id         = instance_id
            msg_cp.campaign_id         = campaign_id
            msg_cp.message_description = message_description
            msg_cp.message             = message
            msg_cp.time_msg            = time_msg
            msg_cp.created_at          = created_at
            msg_cp.customer_id         = customer_id[0]
            msg_cp.media_type          = media_type
            if media_name != '':
                msg_cp.media_name          = media_name
            msg_cp.media_url           = media_url

            msg_cp.save()
            return id

        except Exception as e:
            print(e)
            return False


    def _fetch_messages(self, request, id=None):
        id_customer=request.session.get('customer_user')
        
        if id is not None:
            id_message = f"AND m.id = {id}"
            print(id_message)
        else:
            id_message = f"AND 1 = 1 "

        # format id customers
        id_customer_str = [str(id) for id in id_customer]
        id_customers_clause = f"({', '.join(id_customer_str)})"
        
        # Get infos all messages
        cursor = connection.cursor()
        fetch_messages = (f"SELECT m.id, c.campaigns_name, m.message, m.message_description, m.media_type, m.media_name, m.time_msg, m.campaign_id "
                          f"FROM activeut_messagens_campaigns AS m "
                          f"JOIN activeut_campaigns AS c "
                          f"ON m.campaign_id = c.id "
                          f"WHERE m.customer_id IN {id_customers_clause} "
                          f"{id_message}")
        
        cursor.execute(fetch_messages)
        all_messages = cursor.fetchall()
        connection.close()   
        
        json_all_messages = {}

        for campaign in all_messages:
            id, campaigns_name, message, message_description, media_type, media_name, time_msg, campaign_id = campaign
            json_all_messages[id] = {
                'id': id,
                'campaigns_name': campaigns_name,
                'message_description': message_description,
                'message': message,
                'media_type': media_type,
                'media_name': media_name,
                'time_msg': time_msg,
                'campaign_id': campaign_id
        }
        return json_all_messages
    
    
    def _convertStamp(self, timeSampt=None):
        try:
            if timeSampt is None:
                return timezone.now()
            else:
                messageTimestamp = timezone.datetime.fromtimestamp(int(timeSampt))
                messageTimestamp = timezone.make_aware(messageTimestamp, timezone=timezone.utc)
                messageTimestamp = timezone.localtime(messageTimestamp, timezone=timezone.get_current_timezone())
                return messageTimestamp
        except Exception as e:
            print(f"Error convert timeStamp >>> {e}")
            messageTimestamp = datetime.fromtimestamp(int(timeSampt)).strftime('%Y-%m-%d %H:%M:%S.%f')
            messageTimestamp =  timezone.make_aware(messageTimestamp)
            return messageTimestamp
