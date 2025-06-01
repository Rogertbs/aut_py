import csv, json
import requests, time, threading
from threading import Thread
import multiprocessing
from datetime import datetime
from django.core.cache import cache
from activeut.models import campaigns
from activeut.models import leads_in
from activeut.controllers.timeFrameController import timeFrameController
from datetime import datetime
from django.db import connection




class activeUtController(Thread):
    "Class handle input files and prepare shipping message"

    def __init__(self):
        print("Initiate activeUt")
        self.active_threads = []
        self.tf = timeFrameController()

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
    
    def _processInput(self, campaign_id, csv_file):
        print(f"{csv_file} {campaign_id}")
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
                    #'msg': msg_out.replace("{name}", str(tmp[0])),
                    "id_lead": int(new_lead.id)
                }
                i = i+1
            print(json_data)
        except Exception as e:
            print(f"Error in process csv >>> {e}")
            return None
        return json_data
    
       
    def _sendMessages(self, request):

        try:
            print("In sendMSG")
            campaign_id = request.POST['campaign_id']
            handler = int(request.POST['status'])
            time_msg = 3
            # To Do Falta manipular o tempo time_msg no banco de dados
            print(f"Handler Campaigns action >>> {handler} >>> Campaign id >> {campaign_id}")
            # <<<<< Enable Campaign >>>>>
            if handler == 1:
                print(f"<<< Enabled Campaign {campaign_id} >>> \n")
                
                # Set campaign enable in database
                self._handleCampaign(campaign_id, handler)            
                
                # Get infos campaign enabled
                cursor = connection.cursor()
                fetch_instances = (f"SELECT i.instance_name, i.api_key, i.url, i.enabled, i.limit, i.contract_id, msg.media_type from activeut_campaigns AS camp "
                                f"JOIN activeut_messagens_campaigns as msg " 
                                f"ON camp.id = msg.campaign_id "
                                f"JOIN activeut_instances as i "
                                f"ON i.id = msg.instance_id " 
                                f"WHERE camp.id = {campaign_id}")
               
                cursor.execute(fetch_instances)
                result = cursor.fetchall()
                connection.close()
                
                for instances in result:
                    INSTANCE = instances[0]
                    APIKEY = instances[1]
                    URL = instances[2]
                    MEDIA_TYPE = instances[6]
                
                #print(f"{INSTANCE} \n")
                #print(f"{APIKEY} \n")
                #print(f"{URL} \n")
                #print(f"{MEDIA_TYPE} \n")
                
                if MEDIA_TYPE == 'media':
                    URL = f"{URL}/sendMedia/{INSTANCE}"
                elif MEDIA_TYPE == 'text':
                    URL = f"{URL}/sendText/{INSTANCE}" 
                
                HEADERS = {
                    'apikey': APIKEY,
                    'Content-Type': 'application/json'
                    }
                
                '''
                INSTANCE_UNIFY = 'unifytalk'
                INSTANCE_TATHI = 'thathi'
                APIKEY_TATHI = "175CEC56-1841-4D8D-B851-48E6F700A43C"
                APIKEY_UNIFY = "04093234-AE39-4F1A-965D-8629E7D07616"
                URL = f"http://painel.unifytalk.com.br:8055/message/sendText/{INSTANCE_UNIFY}"
                HEADERS = {
                        'apikey': APIKEY_UNIFY,
                        'Content-Type': 'application/json'
                    }
                '''
            elif int(handler) == 0:
                try:
                    return self._destroyCampaignProcess(campaign_id)
                except Exception as e:
                    print(f"Error Disable Campaign {campaign_id} >> {e}")
                    return 0

            # __ Get all leads whit id campaign information param
            try:
                cursor = connection.cursor()  
                query = (f"SELECT camp.id, le.lead_name, le.lead_number, msg.message, le.send_status, le.id, msg.media_name FROM activeut_leads_in AS le " 
                                f"JOIN activeut_campaigns AS camp "
                                f"ON camp.id = le.id_campaign "
                                f"JOIN activeut_messagens_campaigns AS msg "
                                f"ON camp.id = msg.campaign_id "
                                f"WHERE camp.id = {int(campaign_id)} AND "
                                f"le.send_status = ''")
                
                cursor.execute(query)
                result = cursor.fetchall()
                connection.close()

                if len(result) == 0:
                    print(f"Not found leads to this campaign  >> {campaign_id}")
                    self._destroyCampaignProcess(campaign_id)
                    return 0
                    
                
            except Exception as e:
                print(f"Error query >> {e}")
            
            try:
                json_data_new = {}
                x = 0
                for row in result:
                    json_data_new[x] = {
                        'id_campaign': row[0],
                        'lead_name': row[1],
                        'lead_number': row[2],
                        'id_lead': row[5],
                        'msg': str(row[3]).replace("{name}", str(row[1])),
                        'media_name': row[6]
                    }
                    x = x+1
                    print(f"Json new >> {json_data_new} >> Campaing_id >> {campaign_id}")
                
            except Exception as e:
                # Set campaign disabled in database
                self._destroyCampaignProcess(campaign_id)
                print(f"Error create json leads campaigns >> {e}")
            
           
            
            def _ast_sending(**kwargs):
                try:
                    #import pdb; pdb.set_trace()
                    time.sleep(3)
                    campaign_id = kwargs['campaign_id']
                    json_data = kwargs['json_data']
                    time_msg = kwargs['time_msg']
                    sending_campaigns = cache.get(str(campaign_id))
                    print(f"Check if campaign is in Cache before initiate ast_sending >>> {sending_campaigns}")
                    if sending_campaigns is None:
                        
                        # initiate loop for sended messagens campaign
                        count = len(json_data)
                        for lead in json_data:
                            while not self.tf._time_frame(campaign_id):
                                print(f"[{datetime.now()}] Fora do horário. Aguardando...")
                                time.sleep(250)
                            count = count - 1
                            print(f"{lead} << Log >> {json_data[lead]['lead_name']} >> Count {count} << timestamp {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                            if MEDIA_TYPE == 'text':
                                data = {
                                    "number": "55"+json_data[lead]['lead_number'],
                                    "options": {
                                        "delay": 3000,
                                        "presence": "composing"
                                    },
                                    "text": json_data[lead]['msg']
                                }
                            elif MEDIA_TYPE == 'media':
                                data = {
                                    "number": "55"+json_data[lead]['lead_number'],
                                    "options": {
                                        "delay": 3000,
                                        "presence": "composing"
                                    },
                                    "mediatype": "image",
                                    "mimetype": "image/png",
                                    "caption": json_data[lead]['msg'],
                                    "media": f"http://200.152.191.137:8088/media/{json_data[lead]['media_name']}",
                                    "fileName": "boleto.png0" 
                                }
                                #print(data)
                            try:
                                response = requests.post(URL, headers=HEADERS, data=json.dumps(data), timeout=10)
                                print(f"{response.status_code}")
                                print(f"{response.json()}")
                                print(f"Sended Data simulate >> {data}")
                                res = response.json()
                                # Save status sended
                                if int(response.status_code) == 201:
                                    messageTimestamp = self._convertStamp(res['messageTimestamp'])
                                    lead_to_update = leads_in.objects.filter(lead_number=json_data[lead]['lead_number'],
                                                                             id_campaign=int(json_data[lead]['id_campaign']),
                                                                             id=int(json_data[lead]['id_lead'])).order_by('-created_at')[:1]
                                    
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
                                        obj.send_status = res['response']['message'][0]['exists']
                                        obj.send_timestamp = messageTimestamp
                                        obj.save()
                                                                    
                                #if count == 1:      
                                time.sleep(int(time_msg) * 60)
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
                                time.sleep(29)
                                
                    else:
                        print(f"Cache existe campaign >>> {sending_campaigns}")
                        
                except Exception as e:
                    print(f"Error ast_sending >> {e}")
                    # Set campaign disabled in database
                    #self._handleCampaign(campaign_id, 0)
                    self._destroyCampaignProcess(campaign_id)   
                    print(f">>>> (Exception in Sended Campaign End - Campaign {campaign_id} <<<<<< \n")

                # Set campaign disabled in database
                self._destroyCampaignProcess(campaign_id)
                #self._handleCampaign(campaign_id, 0)
                print(f">>>>>> End - Campaign Success {campaign_id} <<<<<<<< \n")
                
                
            try:
                sending_campaigns = cache.get(str(campaign_id))
                print(f"Check if campaign is in Cache before initiate >>> {sending_campaigns}")
                if sending_campaigns is None:
                    campaign_thread = multiprocessing.Process(target=_ast_sending,
                                                              kwargs={'json_data' : json_data_new,
                                                                      'time_msg': time_msg,
                                                                      'campaign_id': campaign_id})
                    campaign_thread.start()
                    
                    print(f"Initiate thread campaign {cache.get(str(campaign_id))} "
                          f">> {threading.current_thread()} "
                          f">> Ident thread >> {threading.get_ident} \n")
                    
                    cache.set(str(campaign_id), campaign_thread.pid, timeout=86400) # 24 hours
                    
                    print(f">>>>>> Thread Seted >>>> {cache.get(str(campaign_id))}")

                    # Set name in process
                    current_process = multiprocessing.current_process()
                    print(f">>>>>> Original process name: {current_process.name} >>>>>> \n")
                    # Set a new name for the main process
                    current_process.name = f"Campaign-{campaign_id}"
                    print(f">>>>>> New process name: {current_process} >>>>>> \n")

                    for process in multiprocessing.active_children():
                        print(f">>>>>> Status process PID {process} >>>>>> \n")
                else:
                    print(f">>>>>> Thread already exists >>>> {str(campaign_id)} >>>>>> n")

                        
            except Exception as e:
                # Set campaign disabled in database
                self._destroyCampaignProcess(campaign_id)
                self._handleCampaign(campaign_id, 0)
                print(f"returned Error initiate Thread / Campaign: {e} \n")
                return None
 
        except Exception as e:
            # Set campaign disabled in database
            self._destroyCampaignProcess(campaign_id)
            self._handleCampaign(campaign_id, 0)
            print(f"Error in ast sended Campaigns >> {e}")
            return None
        print("ok-end")
    
    
    def _handleCampaign(self, campaign_id=int, handler=int):
        try:
            # Set campaign disabled in database
            campaign = campaigns.objects.get(id=campaign_id)
            print(campaign)
            print(f">>>>>>>>> Set campaign Handler >>> {handler}")
            campaign.enabled = handler
            campaign.save()
            #print(f">>>>>>>>> Set campaign {campaign_id} Handler Success >>> {handler}")
            return True
        except Exception as e:
            print(f">>>>>>>>> Set campaign {campaign_id} Handler Error >>> {handler} >>> {e}")
            return False
    
    def _destroyCampaignProcess(self, campaign_id=int):
        try:
            print(f"<<<<<<<<< Initiate Destroy PID Campaign {campaign_id} >>>>>>>>> \n")
            print(f"Handler Campaigns action Disabled >>> Campaign id >> {campaign_id} \n Cache >> {cache.get(str(campaign_id))}")
            #from django.core.cache.backends import locmem
            #print(f"caches >>>>>> {locmem._caches}")
            if cache.get(str(campaign_id)) is not None:
                campaign_process = multiprocessing.current_process()
                print(f"<<<<<<<<<<< {campaign_process} <<<<<<<<<<< \n") 
                thread_id = cache.get(str(campaign_id))
                print(f"<<<<<<<<<<< thread_id get cache >> {thread_id} <<<<<<<<<<< \n")
                if thread_id:
                    print(f"<<<<<<<<<<< Thread id existis {thread_id} <<<<<<<<<<< \n")
                    for process in multiprocessing.active_children():
                        print(f"<<<<<<<<<<< Try search process with PID {thread_id} <<<<<<<<<<< \n")
                        if int(process.pid) == int(thread_id):
                            print(f"<<<<<<<<<<< Found process with PID {thread_id} <<<<<<<<<<< \n")
                            process.terminate()
                            process.join()
                            print(f"<<<<<<<<<<< Terminad process pid-id {thread_id} campaigns >> {campaign_id} <<<<<<<<<<< \n")
                            cache.delete(str(campaign_id))
                            
                            # Set campaign disabled in database
                            self._handleCampaign(campaign_id, 0)
                            print(f"<<<<< Campaign {campaign_id} finalyzed with success ? {campaign_process} ? >>> \n")
                            return 0
                else:
                    print(f"<<<<< Not found thread_id >> {thread_id} >>>")

                
            # Set campaign disabled in database
            self._handleCampaign(campaign_id, 0)
            return 0
        except Exception as e:
            print(f"Error Disable Campaign {campaign_id} >> {e}")
            return 0
        
    def _convertStamp(self, timeSampt=None):
        try:
            if timeSampt is None:
                return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            else:
                return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        except Exception as e:
            print(f"Error convert timeStamp >>> {e}")
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    
    
        

            
                

