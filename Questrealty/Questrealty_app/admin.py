from django.contrib import admin
from .models import Payment, Room, Message

# Register your models here.
admin.site.register(Payment)
admin.site.register(Room)
admin.site.register(Message)