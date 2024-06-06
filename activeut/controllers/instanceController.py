from activeut.models import instances

class instanceController():
    "Class handle instances"

    def __init__(self):
        print("Initiate Instances Class")

    def _fetch_instances(self, request):
        all_instances = instances.objects.filter(id_customer__in=request.session.get('customer_user'))   
        
        json_all_instances = {}
        for x in all_instances:
            print(x.id)
            print(x.instance_name)
            json_all_instances[x] = {
                "id": x.id,
                "instance_name": x.instance_name
            }
        
        return json_all_instances