from email import message
from django.contrib.auth.models import User
from turtle import title
from django.db import models
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.
    
class Review(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to='upload/pics')
    content = models.TextField()
    
    def __str__(self):
        return self.name
    
class Wallet(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE)
    currency = models.CharField(max_length=50, default='NGN')
    created_at = models.DateTimeField(default=timezone.now, null=True)


    def __str__(self):
        return self.user.__str__()

class WalletTransaction(models.Model):

    TRANSACTION_TYPES = (
        ('deposit', 'deposit'),
        ('transfer', 'transfer'),
        ('withdraw', 'withdraw'),
    )
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=200, null=True,  choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=100, null=True, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now, null=True)
    status = models.CharField(max_length=100, default="pending")
    paystack_payment_reference = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.wallet.user.__str__()
    

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
   
