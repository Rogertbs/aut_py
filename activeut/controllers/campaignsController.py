import csv, json
import requests, time, threading
from threading import Thread
from datetime import datetime
from django.core.cache import cache
from activeut.models import campaigns
from activeut.models import leads_in
from datetime import datetime
from django.utils import timezone

class campaignsController(Thread):
    "Class handle input campaigns"

    def __init__(self):
        print("Initiate Campaigns")
    
    def _createCampaing(self, request):
        try:
            campaigns_name = request.POST['campaigns_name']
            campaigns_describre = request.POST['campaigns_describe']
            enabled = request.POST['enabled'] if request.POST['enabled'] == 1 else 0
            created_at = self._convertStamp()
            customer_id = request.session.get('customer_user')
            # Create an instance of YourModel
            new_campaign = campaigns(campaigns_name=campaigns_name,
                                    campaigns_describre=campaigns_describre,
                                        enabled=enabled,
                                        created_at=created_at,
                                        customer_id=customer_id)

            # Save the instance to the database
            result = new_campaign.save()
            print(result)
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
