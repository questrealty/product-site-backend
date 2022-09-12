from django.contrib import admin

# Register your models here.
from .models import PropertyImages, ListedProperties
admin.site.register(PropertyImages)
admin.site.register(ListedProperties)