from threading import Thread
from datetime import datetime
from django.core.cache import cache
from activeut.models import campaigns
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
            instance_id=request.POST['instanceSelect']
            created_at = self._convertStamp()
            customer_id = request.session.get('customer_main')
            new_campaign = campaigns(campaigns_name=campaigns_name,
                                    campaigns_describre=campaigns_describre,
                                        enabled=0,
                                        created_at=created_at,
                                        customer_id=customer_id[0], ### Todo erro ao salvar pq agora tem uma lista [1,2] ver o que vai fazer???
                                        instance_id=instance_id)

            # Save the instance to the database
            result = new_campaign.save()
            print(result)
        except Exception as e:
            print(e)
            return False
        return True
    

    def _fetch_campaigns(self, request):
        all_campaigns = campaigns.objects.filter(customer_id__in=request.session.get('customer_user')).order_by('-created_at')   
        
        json_all_campaigns = {}
        for x in all_campaigns:
            json_all_campaigns[x] = {
                "id": x.id,
                "campaign_name": x.campaigns_name,
                "campaign_describe": x.campaigns_describre
            }
        return json_all_campaigns

    
    
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
