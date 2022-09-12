from django.db import models

# Create your models here.

class PropertyTypes(models.Model):
    property_type_name = models.CharField(max_length=70, blank=False, default='')
