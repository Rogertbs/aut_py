import ast
from activeut.models import customers

class customersController():
    "Class handle input customers"

    def __init__(self):
        print("Initiate Customers")
    
    def _setCustomerUser(self, user_session_id, request):

        customers_ids = []
        customers_all = customers.objects.all()
        for customer in customers_all:
            users_id_list = ast.literal_eval(customer.users_id)
            for list_id in users_id_list:
                if user_session_id == list_id:
                    print(f"achei {user_session_id} in {users_id_list} Set session customer >> {customer.id}")
                    # set id customer in session user logged
                    #request.session['customer_user'] = customer.id
                    customers_ids.append(customer.id)
        
        request.session['customer_user'] = customers_ids
        print(f"session['customer_user'] >>>>> {request.session['customer_user']}")

        # set id main
        request.session['customer_main'] = self._getCustomerMain(str(user_session_id))
        print(f"Session id main >>> {request.session['customer_main']}")
    

    def _getCustomerMain(self, id):

        # User : Id_main
        customers_main = {
            "1": [1],
            "2": [2]
        }

        return customers_main[id]