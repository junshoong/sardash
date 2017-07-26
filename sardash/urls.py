"""sardash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from main.views import get_sar_data
from main.views import download
from main.views import file_list
from sardash.views import HomeView

ip_regex = r'(?P<ip>((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9]))'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^{}/$'.format(ip_regex), HomeView.as_view(), name='home'),
    url(r'^{}/(?P<resource>cpu|memory|paging)/$'.format(ip_regex), get_sar_data, name="get_sar_data"),
    url(r'^{}/list/$'.format(ip_regex), file_list, name="file_list"),
    url(r'^{}/(?P<file_name>sa\d+)/$'.format(ip_regex), download, name="download"),
]
