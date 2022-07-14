from rest_framework import serializers 
from property_types.models import PropertyTypes

class PropertyTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyTypes
        fields = ('id', 'property_type_name')