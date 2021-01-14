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
from django.urls import path, include

app_name = 'app_root'

urlpatterns = [
    path('', include('app_root.landing.urls')),
    path('helpers/', include('app_root.helpers.urls')),
    path('keywords/', include('app_root.keywords.urls')),
    path('gameinfos/', include('app_root.gameinfos.urls')),
    path('analysis/', include('app_root.analysis.urls')),
]
