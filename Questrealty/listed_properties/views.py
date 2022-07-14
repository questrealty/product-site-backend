from pydoc import visiblename
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status, viewsets, parsers
from rest_framework.decorators import api_view
from listed_properties.models import ListedProperties, PropertyImages
from listed_properties.serializers import ListedPropertiesSerializer, PropertyImagesSerializer
import django_filters.rest_framework as filter
from rest_framework import filters



class PropertyFilter(filter.FilterSet):
    """Filter for Books by Price"""
    price = filter.RangeFilter(field_name='price')

    class Meta:
        model = ListedProperties
        fields = ['propertytypeid', 'userid', 'price']



# # Range: Books between 5€ and 15€
# f = F({'price_min': '5', 'price_max': '15'}, queryset=qs)

# # Min-Only: Books costing more the 11€
# f = F({'price_min': '11'}, queryset=qs)

# # Max-Only: Books costing less than 19€
# f = F({'price_max': '19'}, queryset=qs)

class ListedPropertiesViewSet(viewsets.ModelViewSet):
    queryset = ListedProperties.objects.all()
    serializer_class = ListedPropertiesSerializer
    filter_backends = [filter.DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['propertytypeid', 'userid']
    search_fields = ['title']
    filterset_class = PropertyFilter
    # filter_fields = ["propertytypeid"]

class PropertyImagesViewSet(viewsets.ModelViewSet):
    queryset = PropertyImages.objects.all()
    serializer_class = PropertyImagesSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
