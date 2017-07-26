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
from main.views import get_sar_cpu
from main.views import get_sar_mem
from main.views import get_sar_paging
from main.views import download_sa
from sardash.views import HomeView

ip_regex = r'(?P<ip>((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9]))'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^{}/$'.format(ip_regex), HomeView.as_view(), name='home'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^{}/cpu/$'.format(ip_regex), get_sar_cpu, name="get_sar_cpu"),
    url(r'^cpu/$', get_sar_cpu, name="get_sar_cpu"),
    url(r'^{}/mem/$'.format(ip_regex), get_sar_mem, name="get_sar_mem"),
    url(r'^mem/$', get_sar_mem, name="get_sar_mem"),
    url(r'^{}/paging/$'.format(ip_regex), get_sar_paging, name="get_sar_paging"),
    url(r'^paging/$', get_sar_paging, name="get_sar_paging"),
    url(r'^{}/(?P<file_name>sa\d+)/$'.format(ip_regex), download_sa, name="file"),
]
