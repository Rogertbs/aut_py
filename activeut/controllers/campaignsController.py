from threading import Thread
from datetime import datetime
from activeut.models import campaigns
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import connection

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
            new_campaign.save()
            print(f"Result save campaign >>> {new_campaign}")
            return new_campaign
        except Exception as e:
            print(e)
            return False
        return True
    
    
    def _fetch_campaigns(self, request, id=None):
        try:
            id_customer = ",".join(map(str, request.session.get('customer_user')))
            
            if id is not None:
                q_id = f"AND c.id = {id}"
            else:
                q_id = f"AND 1"

            all_campaigns = (f"SELECT c.id, c.campaigns_name, c.campaigns_describre, c.instance_id, i.instance_name, c.enabled "
                                f"FROM activeut_campaigns AS c JOIN activeut_instances AS i ON c.instance_id = i.id "
                                f"WHERE c.customer_id IN ({id_customer}) "
                                f"{q_id} "
                                f"ORDER BY c.id DESC")

            cursor = connection.cursor()
            cursor.execute(all_campaigns)
            result = cursor.fetchall()
            connection.close()

            res_all_campaigns = {}
            for camp in result:
                id, campaigns_name, campaigns_describe, instance_id, instance_name, enabled  = camp
                res_all_campaigns[id] = {
                    "id": id,
                    "campaign_name": campaigns_name,
                    "campaign_describre": campaigns_describe,
                    "instance_id": instance_id,
                    "instance_name": instance_name,
                    "enabled": enabled
                }
            
            return res_all_campaigns
        except Exception as e:
            print(e)
            return 0
        

    def _campaign_update(self, request, id=None):
        try:
            campaigns_name = request.POST['campaigns_name']
            campaigns_describre = request.POST['campaigns_describe']
            instance_id=request.POST['instanceSelect']
            customer_id = request.session.get('customer_main')
 
            # Update 
            camp_up = get_object_or_404(campaigns, id=id)
            camp_up.campaigns_name       = campaigns_name
            camp_up.campaigns_describre  = campaigns_describre
            camp_up.customer_id          = customer_id[0]
            camp_up.instance_id          = instance_id

            camp_up.save()
            return True
        except Exception as e:
            print(e)
            return False
    
    
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
