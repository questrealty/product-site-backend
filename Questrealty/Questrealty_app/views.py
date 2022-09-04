from email import message
from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse, JsonResponse 
from django.shortcuts import get_object_or_404, redirect, render
from .form import PaymentForm
from django.conf import settings
from .models import Payment, Review, Room, Message
from django.contrib import messages
from django.core import mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os


# Create your views here.

def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            pay = form.save()
            return render(request, 'payment.html', {'pay': pay, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        form = PaymentForm()
    return render(request, 'initiate_pay.html', {'form':form})


def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.error(request, 'Verification Failed')
    else:
        
        messages.success(request, 'Verification Successful')
    return redirect('Questrealty_app:initiate-payment')


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

def chat(request):
    return render(request, 'chat.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
    
def review(request):
    review = Review.objects.all()
    return render(request, 'review.html', {'review': review})