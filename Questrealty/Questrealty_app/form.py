from email import message
from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    fullname = forms.CharField( widget=forms.TextInput(attrs={'class': 'input--style-4', 'label': 'Full Name', 'placeholder': 'Enter your full name'}))
    amount = forms.IntegerField( widget=forms.TextInput(attrs={'class': 'input--style-4', 'label': 'Amount', 'placeholder': 'Enter amount'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'input--style-4',
        'placeholder': 'Enter your email',
        'label': 'Email',
        'id': 'usercomment',

        
    }))
    class Meta():
        model = Payment
        fields = ['fullname', 'email', 'amount']
        
