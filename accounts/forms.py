from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your forms here.


# REGISTERATION FORM
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Please enter a valid email.')
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password1 = forms.CharField()
    password2 = forms.CharField()
    country_code = forms.IntegerField()
    format_digits = forms.IntegerField()
    is_agent = forms.BooleanField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "country_code", "format_digits", "password1", "password2", "is_agent")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



# CHANGE PASSWORD FORM
class ChangePasswordForm(SetPasswordForm):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))
    
    class Meta:
        model = User
        fields = ('new password, confirm_new_password')
                


# LOGIN USER FORM
class LoginUserForm(AuthenticationForm):
        def __init__(self, *args, **kwargs):
                super().__init__( *args, **kwargs)
                
                self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email address'})
                self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password'})
        class Meta:
            fields = ['email', 'password']


# UPDATE PROFILE FORM
class UpdateProfileForm(UserChangeForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    country_code = forms.IntegerField()
    format_digits = forms.IntegerField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "country_code", "format_digits")