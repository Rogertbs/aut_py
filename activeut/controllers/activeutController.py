import csv, json
import requests, time, threading
from threading import Thread

from datetime import datetime
from django.core.cache import cache
from datetime import datetime



class activeUtController(Thread):
    "Class handle input files and prepare shipping message"

    def __init__(self):
        print("Initiate activeUt")
        self.active_threads = []

    
    def _processInput(self, msg_out, csv_file):
        print(f"{msg_out} {csv_file}")
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            json_data = {}
            i = 0
            for row in reader:
                tmp = row[0].split(";")
                json_data[i] = { 
                    'id': tmp[0],
                    'name': tmp[1],
                    'number': tmp[2],
                    'msg': msg_out.replace("{name}", str(tmp[1]))
                }
                i = i+1
        except Exception as e:
            print(f"Error in process csv >>> {e}")
            return None
        
        return json_data
    

       
    def _sendMessages(self, time_msg, json_data):

        try:
            URL = 'http://app.unifytalk.com.br:8080/message/sendText/evounifytalk'
            HEADERS = {
                    'apikey': 'B6D711FCDE4D4FD5936544120E713976',
                    'Content-Type': 'application/json'
                }

            def _ast_sending(**kwargs):
                try:
                    # Mock cache campaign
                    campaign_name = 'campaign_name'
                    #campaign_name = kwargs['campaign_name']
                    json_data = kwargs['json_data']
                    time_msg = kwargs['time_msg']
                    sending_campaigns = cache.get('campaign_name')

                    if sending_campaigns is None:
                        # Set cache name campaign 
                        # to do set timeout cache multiple time_msg variable***
                        cache.set('campaign_name', campaign_name, timeout=13600)
                        
                        # initiate loop for sended messagens campaign
                        for lead in json_data:
                            print(f"{lead} <<test>> {json_data[lead]['name']} >>test<< timestamp {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                            data = {
                                "number": json_data[lead]['number'],
                                "options": {
                                    "delay": 3000,
                                    "presence": "composing"
                                },
                                "textMessage": {
                                    "text": json_data[lead]['msg']
                                }
                            }
                            try:
                                response = requests.post(URL, headers=HEADERS, data=json.dumps(data))
                                print(f"Sended Data simulate >> {data}")
                                time.sleep(int(time_msg) * 3)
                            except Exception as e:
                                print("_httpexecute returned Unknown Error: {}".format(str(e)))
                                return None
                    else:
                        print(f"Cache existe campaign >>> {sending_campaigns}")
                        return None
                except Exception as e:
                    print(f"Error ast_sending >> {e}")
                    return None
                print(f"Deleted cache!!! >> >>> End - Campaign <<< ")
                cache.delete('campaign_name')
                
            try:       
                threading.Thread(target=_ast_sending, kwargs={'json_data' : json_data, 'time_msg': time_msg}).start()
                print(f"Initiate thread campaign {cache.get('campaign_name')} >> {threading.current_thread()}")
            except Exception as e:
                print(f"returned Error initiate Thread: {e}")
                return None
 
        except Exception as e:
            print(f"Error in ast sended >> {e}")
            return None
        print("ok-end")


