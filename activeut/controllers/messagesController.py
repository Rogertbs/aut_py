import csv, json
import requests, time, threading
from threading import Thread
from datetime import datetime
from activeut.models import messagens_campaigns
from datetime import datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

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
            campaign_id = request.POST['campaignSelect']
            message_description = request.POST['message_description']
            message = request.POST['message']
            created_at = self._convertStamp()
            customer_id = request.session.get('customer_user')
            media_type = 'media' if request.POST['RadioMedia'] == 'on' else 'text'
            media_name = request.FILES['media'] if len(request.FILES['media']) > 0 else ''
            media_url = 'https://painel.unifytalk.com.br:444/media/'
            # Create an instance of YourModel
            new_campaign = messagens_campaigns(campaign_id=campaign_id,
                                    message_description=message_description,
                                        message=message,
                                        created_at=created_at,
                                        customer_id=customer_id,
                                        media_type=media_type,
                                        media_name=media_name,
                                        media_url=media_url)

            # Save the instance to the database
            result = new_campaign.save()
            print(result)
            
            
            uploaded_file = request.FILES['media']
            fs = FileSystemStorage(location='/var/www/media/')  # Change this to your desired directory
            filename = fs.save(uploaded_file.name, uploaded_file)
            print(filename)
        except Exception as e:
            print(e)
            return False
        return True

    
    
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
