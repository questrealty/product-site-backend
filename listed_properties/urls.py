from django.urls import path, include
from listed_properties import views
from rest_framework.routers import SimpleRouter
from .views import PropertyImagesViewSet, ListedPropertiesViewSet
from Questrealty import settings
from django.conf.urls.static import static

router = SimpleRouter()
router.register('properties', ListedPropertiesViewSet)
router.register('images', PropertyImagesViewSet)

 
urlpatterns = router.urls
if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# [ 
#     path('listedproperties/add', views.properties_list)
    
# ]