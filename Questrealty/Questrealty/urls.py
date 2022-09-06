"""Questrealty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Questrealty_app.urls')),
    path('', include('property_types.urls')),
    path('accounts/', include('django.contrib.auth.urls')), #new
    path('api/', include('rest_framework.urls')),  # new
    path('', include('listed_properties.urls')), # new
    path('', include('accounts.urls')), # new
    path('api/password_reset/', include('django_rest_passwordreset.urls')), #new
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #new
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #new
]
