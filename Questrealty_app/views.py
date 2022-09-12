from email import message
from sqlite3 import Timestamp
from django.http.response import JsonResponse
from django.http import HttpRequest, HttpResponse 
from django.shortcuts import render
from django.contrib import messages
from django.core import mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.conf import settings
from .models import Wallet, WalletTransaction, Review, Message
from  Questrealty_app.serializers import ReviewSerializer, WalletSerializer, DepositSerializer, MessageSerializer, UserSerializer
import requests

User = get_user_model()



class WalletInfo(APIView):
   
    def get(self, request):
        wallet = Wallet.objects.filter(user=request.user.id).first()
        data = WalletSerializer(wallet).data
        return Response(data)


class DepositFunds(APIView):

    def post(self, request):
        serializer = DepositSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        resp = serializer.save()
        return Response(resp)

class VerifyDeposit(APIView):

    def get(self, request, reference):
        transaction = WalletTransaction.objects.get(
        paystack_payment_reference=reference, wallet__user=request.user)
        reference = transaction.paystack_payment_reference
        url = 'https://api.paystack.co/transaction/verify/{}'.format(reference)
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        
        r = requests.get(url, headers=headers)
        resp = r.json()
        if resp['data']['status'] == 'success':
            status = resp['data']['status']
            amount = resp['data']['amount']
            WalletTransaction.objects.filter(paystack_payment_reference=reference).update(status=status,
                                                                                        amount=amount)
            return Response(resp)
        return Response(resp)

class ReviewView(APIView): 
    def get(self, request, *args, **kwargs):
        qs = Review.objects.all()
        serializer = ReviewSerializer(qs, many=True)
        return Response(serializer.data)
    
def contact(request):
    if request.method =='POST':
        name = request.POST.get('name')
        phone_no = request.POST.get('phone-no')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        subject = 'Contact'
        context = {
            'name': name,
            'phone_no': phone_no,
            'email': email,
            'message': message
        }
        html_message = render_to_string('email.html', context)
        plain_message = strip_tags(html_message)
        from_email =  'Questrealty <quest.realty.a@gmail.com>'
        send = mail.send_mail(subject, plain_message, from_email, [
                    'quest.realty.a@gmail.com', email], html_message=html_message, fail_silently=True)
        
        if send:
            messages.success(request, 'Email sent, you will recieve an email shorthly!')
        else:
            messages.error(request, 'Mail not sent')
    return render(request, 'contact.html')

def email(request):
    return render(request, 'email.html')
    
def user_list(request, pk=None):
   
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)    
        if serializer.is_valid():
            serializer.save()                                          
            return JsonResponse(serializer.data, status=201)    
        return JsonResponse(serializer.errors, status=400)  
  
def message_list(request):
    
    if request.method == 'GET':    
        messages = Message.objects.filter()
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)    
        
