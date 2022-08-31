from django.contrib import admin
from .models import Review, Wallet, WalletTransaction, Message

# Register your models here.
admin.site.register(Wallet)
admin.site.register(WalletTransaction)
admin.site.register(Message)
admin.site.register(Review)