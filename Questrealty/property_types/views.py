from pickle import GET
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from property_types.models import PropertyTypes
from property_types.serializers import PropertyTypesSerializer

# Create your views here.

@api_view(['GET'])
def get_propertytypes_list(request):
    if request.method == 'GET':
        property_type = PropertyTypes.objects.all()
        propertytypes_serializer = PropertyTypesSerializer(property_type, many=True)
        return JsonResponse(propertytypes_serializer.data, safe=False)
