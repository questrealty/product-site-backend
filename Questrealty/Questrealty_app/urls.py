from django.urls import path
from django import views
from Questrealty_app import views
from .views import ReviewView, WalletInfo, DepositFunds, VerifyDeposit

app_name = 'Questrealty_app'


urlpatterns = [
    
    
    path('email/', views.email, name='email'), 
    path('review/',ReviewView.as_view(), name='review'), 
    path('deposit/verify/<str:reference>/', VerifyDeposit.as_view()),
    path('deposit/', DepositFunds.as_view()),
    path('wallet_info/', WalletInfo.as_view()),
    path('messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'), 
    path('messages/', views.message_list, name='message-list'), 
    path('users/<int:pk>', views.user_list, name='user-detail'),     
    path('users/', views.user_list, name='user-list'),
]
    


