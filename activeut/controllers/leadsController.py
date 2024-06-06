from activeut.models import leads_in

class leadsController():
    "Class handle input leads Class"

    def __init__(self):
        print("Initiate Leads Class")
    
    def _fetch_leads(self, request):
        print(request.POST)
        if request.method == 'POST':
            campaign_id = request.POST['campaignSelect']
            messages = leads_in.objects.filter(id_campaign=campaign_id).order_by('send_timestamp')
            
            json_messages = {}
            for x in messages:
                print(x.id)
                print(x.lead_name)
                print(x.send_timestamp)
                json_messages[x] = {
                    "id": x.id,
                    "lead_name": x.lead_name,
                    "lead_number": x.lead_number,
                    "send_status": x.send_status,
                    "send_timestamp": x.send_timestamp.strftime('%d/%m/%Y %H:%M:%S') if x.send_timestamp is not None else ''
                }
            return json_messages
        else:
            return ''