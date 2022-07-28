from Questrealty_app import views
from django.urls import path

app_name = 'Questrealty_app'

urlpatterns = [ 
        
    path('', views.chat, name='chat'),    
    path('checkview', views.checkview, name='checkview'), 
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('contact/', views.contact, name='contact-us'),
    path('email/', views.email, name='email'), 
    path('review/',views.review, name='review'), 
    path('initiate_pay/', views.initiate_payment, name='initiate-payment'), 
    path('<str:room>/', views.room, name='room'), 
    path('<str:ref>/', views.verify_payment, name='verify-payment'),  
      
    
    
    
    
    
    
    
    
    
   
   
   
    
    
]
