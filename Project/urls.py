
from django.contrib import admin
from django.conf.urls import url, include

import Common.urls as common_urls
import Shop.urls as shop_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(common_urls)),
    url(r'^', include(shop_urls)),


]
