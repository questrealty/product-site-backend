from Questrealty_app import views
from django.urls import path

app_name = 'Questrealty_app'

urlpatterns = [
    path('contact/', views.contact, name='contact-us'),
    path('email/', views.email, name='email'),
    path('checkroom/', views.checkRoom, name='checkroom'),
    path('chat/', views.chat, name='chat-box'),
    path('<str:room>/', views.room, name='room'),
    path('', views.initiate_payment, name='initiate-payment'),
    path('<str:ref>/', views.verify_payment, name='verify-payment'),
    
   
   
   
    
    
]
