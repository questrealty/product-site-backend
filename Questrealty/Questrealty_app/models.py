from email import message
# from turtle import title
from django.db import models
from django.dispatch import receiver
from django.forms import CharField
import secrets
from .paystack import PayStack

# Create your models here.

class Payment(models.Model):
    
    fullname = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta():
        ordering = ('-date',)
        
    def __str__(self):
        return f"payment: {self.amount}"
    
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs) 
        
    def amount_value(self) -> int:
        return self.amount *100       
        
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
            
class Room(models.Model):
    name = models.CharField(max_length=200) 
    
    def __str__(self):
        return self.name
         
class Message(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=10000)
    room = models.CharField(max_length=10000)
    
    def __str__(self):
        return self.value
    
class Review(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to='upload/pics')
    content = models.TextField()
    
    def __str__(self):
        return self.name
    
    