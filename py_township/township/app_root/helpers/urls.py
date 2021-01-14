"""py_township URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from app_root.helpers.views import HexToBinaryView, Base64EncodeDecodeView, GzipCompressUncompressView, \
    FlowView_fetch_data, FlowView_fetch_city

app_name = 'helpers'

urlpatterns = [
    path('hex2bin/', HexToBinaryView.as_view(), name='hex2bin'),
    path('base64/', Base64EncodeDecodeView.as_view(), name='base64'),
    path('gzip/', GzipCompressUncompressView.as_view(), name='gzip'),
    path('flow/fetch_data/', FlowView_fetch_data.as_view(), name='flow_fetch_data'),
    path('flow/fetch_city/', FlowView_fetch_city.as_view(), name='flow_fetch_city'),
]
