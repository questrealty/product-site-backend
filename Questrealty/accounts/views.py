from email.policy import HTTP
from django.shortcuts import render, redirect
from .models import NewUser
from .forms import NewUserForm, ChangePasswordForm, LoginUserForm, UpdateProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView


# TO REGISTER
class NewUserView(SuccessMessageMixin,generic.CreateView):
    form_class = NewUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Please enter details properly.")
        return redirect('home')

def Register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        # Check if passwords match
        if NewUser.password1 == NewUser.password2:
        # Check if email already exists
            if User.objects.filter(email=NewUser.email).exists():
                messages.error(request, 'This email already exists')
                return redirect('register')
            else:
                # Everything passed
                form.is_valid()
                form.save()
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                user = authenticate(email=email, password=password)
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("agent-dashboard")
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        form = NewUserForm()
        messages.error(request, "Unsuccessful registration.")
        return redirect('register')

    # return render (request=request, template_name="accounts/register.html", context={"register_form":form})


def RegisterAgent(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        # Check if passwords match
        if NewUser.password1 == NewUser.password2:
        # Check if email already exists
            if User.objects.filter(email=NewUser.email).exists():
                messages.error(request, 'This email already exists')
                return redirect('register')
            else:
                # Everything passed
                form.is_valid()
                form.save()
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                user = authenticate(email=email, password=password)
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("agent-dashboard")
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        form = NewUserForm()
        messages.error(request, "Unsuccessful registration.")
        return redirect('register')
    # return render (request=request, template_name="accounts/register.html", context={"register_form":form})

# TO LOGIN
class LogIn(generic.View):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

def Login(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('cust-dashboard')
        else:
            messages.success(request, "Unsuccessful Login")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def LoginAgent(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('agent-dashboard')
        else:
            messages.success(request, "Unsuccessful Login")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


# TO LOGOUT
def Logout(request):
    logout(request)
    messages.success(request, "You were logged out")
    return redirect('home')


# TO UPDATE PROFILE
class UpdateUserView(generic.UpdateView):
    form_class = UpdateProfileForm
    template_name = 'accounts/update_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Please submit the form carefully.")
        return redirect('home')


# TO DISPLAY USER PROFILE check
class UserProfile(generic.View):
    model = NewUser
    template_name = 'accounts/profile.html'

    def profile(self, request, first_name):
        user_related_data = NewUser.objects.filter(pk= first_name)
        context = {
            "user_related_data":user_related_data
        }
        return render(request, self.template_name, context)


# TO DELETE ACCOUNT
class DeleteAccount(SuccessMessageMixin, generic.DeleteView):
    model = User
    template_name = 'accounts/delete_user.html'
    success_message = "User has been deleted"
    success_url = reverse_lazy('home')


# TO CHANGE PASSWORD
class ChangePassword(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('Password Success')

    def password_success(request):
        return render(request, "accounts/password_change_success.html")