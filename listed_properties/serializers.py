from pyexpat import model
from rest_framework import serializers 
from listed_properties.models import ListedProperties, PropertyImages

class ListedPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListedProperties
        fields = ('userid','propertytypeid','title', 'details','location', 'sold', 'for_rent', 'property_size', 'bedrooms', 'bathrooms', 'price')


class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ('property_id', 'image')