import ast
from django.core.cache import cache
from activeut.models import campaigns
from activeut.models import leads_in
from activeut.models import customers
from datetime import datetime
from django.db import connection

class dashboardsController():
    "Class dashboards"

    def __init__(self):
        print("Initiate Dashboards")
    
    def _getTotalDeliverd(self, request):
        
        id_customer=request.session.get('customer_user')
        # Get infos all messages
        cursor = connection.cursor()
        qtd_delivered = (f"SELECT COUNT(l.id) AS 'qtd_delivered' FROM activeut_campaigns AS c "
                          f"INNER JOIN activeut_leads_in AS l "
                          f"ON c.id = l.id_campaign "
                          f"WHERE c.enabled = 1 AND c.customer_id = {id_customer} "
                          f"AND l.send_status = 'PENDING'")
        
        cursor.execute(qtd_delivered)
        qtd_delivered = cursor.fetchall()
        connection.close()   
        if len(qtd_delivered) > 0:
            return int(qtd_delivered[0][0])
        return int(0)

        
    def _getTotalSent(self, request):
    
        id_customer=request.session.get('customer_user')
        # Get infos all messages
        cursor = connection.cursor()
        q_qtd_sent = (f"SELECT COUNT(l.id) as 'qtd_sent' FROM activeut_campaigns AS c "
                         f"INNER JOIN activeut_leads_in AS l "
                         f"ON c.id = l.id_campaign "
                         f"WHERE c.enabled = 1 AND c.customer_id = {id_customer}")
        
        cursor.execute(q_qtd_sent)
        qtd_sent = cursor.fetchall()
        connection.close()   
        if len(qtd_sent) > 0:
            return int(qtd_sent[0][0])
        return int(0)
    
    def _getTotalFalse(self, request):
    
        id_customer=request.session.get('customer_user')
        # Get infos all messages
        cursor = connection.cursor()
        q_qtd_false = (f"SELECT COUNT(l.id) as 'qtd_false' FROM activeut_campaigns AS c "
                         f"INNER JOIN activeut_leads_in AS l "
                         f"ON c.id = l.id_campaign "
                         f"WHERE c.enabled = 1 AND c.customer_id = {id_customer} "
                         f"AND l.send_status = 'False'")
        
        cursor.execute(q_qtd_false)
        qtd_false = cursor.fetchall()
        connection.close()   
        if len(qtd_false) > 0:
            return int(qtd_false[0][0])
        return int(0)
    
    def _getTotalActive(self, request):
    
        id_customer=request.session.get('customer_user')
        # Get infos all messages
        cursor = connection.cursor()
        q_qtd_active = (f"SELECT COUNT(id) FROM activeut_campaigns "
                         f"WHERE enabled = 1 AND "
                         f"customer_id = {id_customer} ")
        
        cursor.execute(q_qtd_active)
        qtd_active = cursor.fetchall()
        connection.close()   
        if len(qtd_active) > 0:
            return int(qtd_active[0][0])
        return int(0)
    
    #outstanding
    
    def _getTotalOutstanding(self, request):
    
        id_customer=request.session.get('customer_user')
        # Get infos all messages
        cursor = connection.cursor()
        q_qtd_outstanding = (f"SELECT COUNT(l.id) AS 'qtd_outstanding' FROM activeut_campaigns AS c "
                             f"INNER JOIN activeut_leads_in AS l "
                             f" ON c.id = l.id_campaign "
                             f"WHERE c.enabled = 1 AND c.customer_id = {id_customer} "
                             f"AND l.send_status = ''")
        
        cursor.execute(q_qtd_outstanding)
        qtd_outstanding = cursor.fetchall()
        connection.close()   
        if len(qtd_outstanding) > 0:
            return int(qtd_outstanding[0][0])
        return int(0)

    # Infos details in realtime
    def _getDetails(self, request):
    
        id_customer=request.session.get('customer_user')
        # Get infos all messages
        cursor = connection.cursor()
        q_qdetails = (f"SELECT l.id, c.campaigns_name, l.lead_name, l.lead_number, l.send_status, l.send_timestamp FROM activeut_campaigns AS c "
                      f"INNER JOIN activeut_leads_in AS l "
                      f"ON c.id = l.id_campaign "
                      f"WHERE c.enabled = 1 "
                      f"AND c.enabled = 1 AND c.customer_id = {id_customer} "
                      f"AND l.send_status <> '' ORDER BY send_timestamp DESC limit 8")
        
        cursor.execute(q_qdetails)
        qtd_details = cursor.fetchall()
        #print(qtd_details)
        connection.close()   
        if len(qtd_details) > 0:
            all_details = {}

            for dt in qtd_details:
                id, campaigns_name, lead_name, lead_number, send_status, send_timestamp = dt
                all_details[id] = {
                    'id': id,
                    'campaigns_name': campaigns_name,
                    'lead_name': lead_name,
                    'lead_number': lead_number,
                    'send_status': send_status,
                    'send_timestamp': send_timestamp.strftime('%d/%m/%Y %H:%M:%S')
                }
            return all_details
        else:
            all_details = {}
            all_details["0"] = {
                    'id': "0",
                    'campaigns_name': "N/A",
                    'lead_name': "N/A",
                    'lead_number': "N/A",
                    'send_status': "N/A",
                    'send_timestamp': "N/A"
            }
            return all_details
    

    def _getDashboard(self, request):

        dash = dashboardsController()

        details =           dash._getDetails(request)
        outstanding =       dash._getTotalOutstanding(request)
        total_actives =     dash._getTotalActive(request)
        total_false =       dash._getTotalFalse(request)
        total_sent =        dash._getTotalSent(request)
        total_delivered =   dash._getTotalDeliverd(request)
        
        result_dashboard = {
            "details": details,
            "outstanding": outstanding,
            "total_actives": total_actives,
            "total_false": total_false,
            "total_sent": total_sent,
            "total_delivered": total_delivered
        }

        return result_dashboard




