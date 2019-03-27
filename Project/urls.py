
from django.contrib import admin
from django.conf.urls import url, include

import Common.urls as common_urls
import Shop.urls as shop_urls

from Shop.views import MainPageView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Common.urls')),
    url(r'^', include('Shop.urls')),
    url(r'^', MainPageView.as_view(), name='main'),

]
