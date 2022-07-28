from django.db import models
from property_types.models import PropertyTypes

# Create your models here.
class ListedProperties(models.Model):
    userid = models.IntegerField(null=False)
    propertytypeid = models.ForeignKey(PropertyTypes, on_delete=models.CASCADE, null=False)
    title = models.TextField(null=False)
    details = models.TextField(null=False)
    location = models.TextField(null=False)
    sold = models.BooleanField(default=False, null=False)
    for_rent = models.BooleanField(default=True, null=False)
    property_size = models.FloatField(null=False)
    bedrooms = models.IntegerField(null=False)
    bathrooms = models.IntegerField(null=False)
    price = models.BigIntegerField(null=False)


class PropertyImages(models.Model):
    property_id = models.ForeignKey(ListedProperties, on_delete=models.CASCADE, null=False)
    image = models.FileField(null=True)

