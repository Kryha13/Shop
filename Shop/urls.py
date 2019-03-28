
from django.contrib import admin
from django.conf.urls import url

from Shop.views import ProductsListView, ProductInfoView
from django_filters.views import FilterView
from Shop.filters import ProductFilter

app_name = 'Shop'

urlpatterns = [
    url(r'^products/$', ProductsListView.as_view(), name='products_list'),
    url(r'^product/(?P<product_id>[0-9]+)/$', ProductInfoView.as_view(), name='product_info'),
    url(r'^search/$', FilterView.as_view(filterset_class=ProductFilter,
                                         template_name='search_product.html'), name='search'),

]