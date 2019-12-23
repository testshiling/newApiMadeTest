"""apimadetest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from apitest.views import *
from apitest.views_index import *

urlpatterns = [
    url(r'^admin/', admin.site.urls, ),
    url(r'^api_cancel_order/', cancel_order),
    url(r'^api_payback_order/', payback_order),
    url(r'^api_others_pay_order/', others_pay_order),
    url(r'^api_pay_order/', pay_order),
    url(r'^api_add_order/', create_order),
    url(r'^api_add_lodgeinfo/', add_lodgeinfo),
    url(r'^api_register/', register),
    url(r'^api_login_get', login_get),
    url(r'^api_login_post/', login_post),
    url(r'^api_demo/', api_demo),
    url(r'^get_lodgeunitInfo', get_lodgeunitInfo),
    url(r'^get_ordertInfo', get_ordertInfo),
    url(r'^pushAPIInfo/', pushAPIInfo),
    url(r'^', welcome),
]
