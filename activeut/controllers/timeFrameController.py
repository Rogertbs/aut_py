from threading import Thread
from activeut.models import time_frames
from datetime import datetime


class timeFrameController(Thread):
    "Class Time Frame"

    def __init__(self):
        print("Initiate Time Frame Class")
    

    def _time_frame(self, campaign_id=int):
        
        get_time_frame = time_frames.objects.filter(campaign_id=campaign_id)

        for hr in get_time_frame:
            hour_begin = hr.hour_begin
            hour_end = hr.hour_end
            day_allowed = hr.days_allowed
        
        print(f"{hour_begin} - {hour_end} - {day_allowed} ")
        now = datetime.now()
        day_week = str(now.weekday())
        hour_now = now.time()
    
        return ( day_week in day_allowed and
             hour_begin <= hour_now <= hour_end )

    def _feth_time_frame(self, campaign_id):
        try:
            get_time_frame = time_frames.objects.filter(campaign_id=campaign_id)
        
            for hr in get_time_frame:
                hour_begin = hr.hour_begin
                hour_end = hr.hour_end
                day_allowed = hr.days_allowed
                message_description = hr.message_description

            response = {
                "hour_begin": hour_begin,
                "hour_end": hour_end,
                "day_allowed": day_allowed.split(","),
                "message_description": message_description
            }
            
            return response
        except Exception as e:
            print(e)
            return False
        
    def _create_time_frame(self, request, campaign_id=None):
        try:
            days_allowed = ",".join(request.POST.getlist('days_allowed'))
            hour_begin = request.POST['hour_begin']
            hour_end = request.POST['hour_end']
            message_description = request.POST['message_description']
            campaign_id = campaign_id
            new_time_frame = time_frames(campaign_id=campaign_id,
                                         message_description=message_description,
                                         days_allowed=days_allowed,
                                         hour_begin=hour_begin,
                                         hour_end=hour_end)
            # Save the instance to the database
            new_time_frame.save()
            return True
        except Exception as e:
            print(e)
            return False
        