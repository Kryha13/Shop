
from django.contrib import admin
from django.conf.urls import url

from Shop.views import MainPageView

app_name = 'Shop'

urlpatterns = [
    url(r'', MainPageView.as_view(), name='main'),

]