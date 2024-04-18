from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('home/', views.home, name='home'),
    
    path('campaigns_index/', views.campaigns_index, name='campaigns_index'),
    path('campaigns_create/', views.campaigns_create, name='campaigns_create'),
    path('handle_campaign/', views.handle_campaign, name='handle_campaign'),
    
    path('messages_index/', views.messages_index, name='messages_index'),
    path('messages_create/', views.messages_create, name='messages_create'),
    
    
    path('leads_in/', views.leads_in, name='leads_in'),
    path('leads_index/', views.leads_index, name='leads_index'),
    #path('/leads_index/leads_index_table/', views.leads_index_table, name='leads_index_table'),
            
    path("", views.index, name="index"),
]