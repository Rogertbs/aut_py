import csv, json
import requests, time, threading
from threading import Thread
from datetime import datetime
from django.core.cache import cache
from activeut.models import campaigns
from activeut.models import leads_in
from datetime import datetime
from django.utils import timezone




class activeUtController(Thread):
    "Class handle input files and prepare shipping message"

    def __init__(self):
        print("Initiate activeUt")
        self.active_threads = []

    """
    # Create an instance of YourModel
    new_object = YourModel(field1='value1', field2='value2')

    # Save the instance to the database
    new_object.save()

    # if dict
    new_object = YourModel(**data)

    #objects filter
    objects_with_conditions = YourModel.objects.filter(condition1=True, condition2=False)
    
    #Sample update
    object_to_update = YourModel.objects.get(id=your_object_id)

    # Modify the object's attributes
    object_to_update.some_field = new_value
    object_to_update.another_field = another_new_value

    # Save the object back to the database
    object_to_update.save()
    
    
    # TO DO logic get databases while send messages 
    SELECT le.lead_name, le.lead_number FROM activeut_leads_in AS le 
    JOIN
    activeut_campaigns AS camp
    ON camp.id = le.id_campaign
    JOIN
    activeut_messagens_campaigns AS msg
    ON camp.id = msg.campaign_id
    WHERE camp.id = 6 AND
    le.send_status = ''
    
    """
    
    def _processInput(self, msg_out, campaign_id, csv_file):
        print(f"{msg_out} {csv_file} {campaign_id}")
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            json_data = {}
            i = 0
            for row in reader:
                tmp = row[0].split(";")
                print(row[0].split(";"))
                print(f"tmp 0 >> {tmp[0]}")
                print(f"tmp 1 >> {tmp[1]}")
                new_lead = leads_in.objects.create(id_campaign = int(campaign_id), lead_name = str(tmp[0]), lead_number = str(tmp[1]))
                print(f"new_lead id >>> {new_lead.id}")
                
                json_data[i] = { 
                    "id_campaign": int(campaign_id),
                    "lead_name": str(tmp[0]),
                    "lead_number": str(tmp[1]),
                    'msg': msg_out.replace("{name}", str(tmp[0])),
                    "id_lead": int(new_lead.id)
                }
                i = i+1
            print(json_data)
        except Exception as e:
            print(f"Error in process csv >>> {e}")
            return None
        return json_data
    
    def _fetch_campaigns(self, request):
        all_campaigns = campaigns.objects.filter(customer_id=request.session.get('customer_user'))   
        
        json_all_campaigns = {}
        for x in all_campaigns:
            print(x.id)
            print(x.campaigns_name)
            json_all_campaigns[x] = {
                "id": x.id,
                "campaign_name": x.campaigns_name,
                "campaign_describe": x.campaigns_describre
            }
        print(type(json_all_campaigns))
        return json_all_campaigns
        
       
    def _sendMessages(self, time_msg, json_data, campaign_id):

        try:
            INSTANCE_UNIFY = 'evounifytalk'
            INSTANCE_TATHI = 'thathi'
            APIKEY_TATHI = "175CEC56-1841-4D8D-B851-48E6F700A43C"
            APIKEY_UNIFY = "B6D711FCDE4D4FD5936544120E713976"
            URL = f"http://app.unifytalk.com.br:8080/message/sendText/{INSTANCE_UNIFY}"
            HEADERS = {
                    'apikey': APIKEY_UNIFY,
                    'Content-Type': 'application/json'
                }
            
            # __ Get all leads whit id campaign information param
            # result = campaigns.objects.extra(
            #     select={'campaigns_name': 'activeut_campaigns.campaigns_name',
            #             'lead_name': 'activeut_leads_in.lead_name',
            #             'lead_number': 'activeut_leads_in.lead_number',
            #             'send_status': 'activeut_leads_in.send_status',
            #             'message': 'activeut_messagens_campaigns.message'
            #             },
            #     tables=['activeut_leads_in', 'activeut_campaigns', 'activeut_messagens_campaigns'],
            #     where=['activeut_campaigns.id = 6', 'activeut_leads_in.send_status = ""'],
            # )
            
            from django.db import connection

            cursor = connection.cursor()    
            cursor.execute("""SELECT camp.campaigns_name, le.lead_name, le.lead_number, le.send_status, msg.message FROM activeut_leads_in AS le 
                            JOIN
                            activeut_campaigns AS camp
                            ON camp.id = le.id_campaign
                            JOIN
                            activeut_messagens_campaigns AS msg
                            ON camp.id = msg.campaign_id
                            WHERE camp.id = 6 AND
                            le.send_status = ''""")
            result = cursor.fetchone()
            print(result)
            for row in result:
                print("AQUI !!!!!")
                print(row)
                # print(row['campaigns_name'],
                #       row['lead_name'],
                #       row['lead_number'],
                #       row['send_status'],
                #       row['message'])
            return True
            def _ast_sending(**kwargs):
                try:
                    # Mock cache campaign
                    campaign_id = kwargs['campaign_id']
                    #campaign_name = kwargs['campaign_name']
                    json_data = kwargs['json_data']
                    time_msg = kwargs['time_msg']
                    sending_campaigns = cache.get('campaign_id')

                    if sending_campaigns is None:
                        # Set cache name campaign 
                        # to do set timeout cache multiple time_msg variable***
                        cache.set('campaign_id', campaign_id, timeout=13600)
                        
                        # initiate loop for sended messagens campaign
                        for lead in json_data:
                            print(f"{lead} <<test>> {json_data[lead]['lead_name']} >>test<< timestamp {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                            data = {
                                "number": json_data[lead]['lead_number'],
                                "options": {
                                    "delay": 3000,
                                    "presence": "composing"
                                },
                                "textMessage": {
                                    "text": json_data[lead]['msg']
                                }
                            }
                            try:
                                response = requests.post(URL, headers=HEADERS, data=json.dumps(data), timeout=4.001)
                                print(f"{response.status_code}")
                                print(f"{response.json()}")
                                print(f"Sended Data simulate >> {data}")
                                res = response.json()
                                # Save status sended
                                if int(response.status_code) == 201:
                                    messageTimestamp = self._convertStamp(res['messageTimestamp'])
                                    lead_to_update = leads_in.objects.filter(lead_number=json_data[lead]['lead_number'],
                                                                             id_campaign=json_data[lead]['id_campaign'],
                                                                             id=json_data[lead]['id_lead']).order_by('-created_at')[:1]
                                    
                                    for obj in lead_to_update:
                                        obj.send_status = res['status']
                                        obj.send_timestamp = messageTimestamp
                                        obj.save()
                                else:                                    
                                    messageTimestamp = self._convertStamp()
                                    lead_to_update = leads_in.objects.filter(lead_number=json_data[lead]['lead_number'],
                                                                             id_campaign=json_data[lead]['id_campaign'],
                                                                             id=json_data[lead]['id_lead']).order_by('-created_at')[:1]
                                    for obj in lead_to_update:
                                        obj.send_status = res['response']['message'][0]
                                        obj.send_timestamp = messageTimestamp
                                        obj.save()
                                                                       
                                      
                                time.sleep(int(time_msg) * 10)
                            except Exception as e:
                                messageTimestamp = self._convertStamp()
                                lead_to_update = leads_in.objects.filter(lead_number=json_data[lead]['lead_number'],
                                                                            id_campaign=json_data[lead]['id_campaign'],
                                                                            id=json_data[lead]['id_lead']).order_by('-created_at')[:1]
                                for obj in lead_to_update:
                                    obj.send_status = 'Api error Timeout'
                                    obj.send_timestamp = messageTimestamp
                                    obj.save()
                                print("_httpexecute returned Unknown Error: {}".format(str(e)))
                                
                    else:
                        print(f"Cache existe campaign >>> {sending_campaigns}")
                        
                except Exception as e:
                    print(f"Error ast_sending >> {e}")
                    
                print(f"Deleted cache!!! >> >>> End - Campaign <<< ")
                cache.delete('campaign_id')
                
            try:       
                threading.Thread(target=_ast_sending, kwargs={'json_data' : json_data, 'time_msg': time_msg, 'campaign_id': campaign_id}).start()
                print(f"Initiate thread campaign {cache.get('campaign_id')} >> {threading.current_thread()}")
            except Exception as e:
                print(f"returned Error initiate Thread: {e}")
                return None
 
        except Exception as e:
            print(f"Error in ast sended >> {e}")
            return None
        print("ok-end")
        
        
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
                

