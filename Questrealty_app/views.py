from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone = request.POST['phone']

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email Already Registered!!")
        return redirect('home')

    if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')

    myuser = User.objects.create_user(email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        return render(request, "authentication/login.html")
def login(request):
     if request.method == 'POST':
        return render(request, "authentication/login.html")

def logout(request):
    pass