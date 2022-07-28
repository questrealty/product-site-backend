from django.urls import path, include
from property_types import views 
 
urlpatterns = [ 
    path('propertytypes/all', views.get_propertytypes_list)
    
]