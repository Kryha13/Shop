
from django.conf.urls import url

from Shop.views import ProductsListView, ProductInfoView, AddProductView, EditProductView, DeleteProductView
from django_filters.views import FilterView
from Shop.filters import ProductFilter

app_name = 'Shop'

urlpatterns = [
    url(r'^products/$', ProductsListView.as_view(), name='products_list'),
    url(r'^product/(?P<product_id>[0-9]+)/$', ProductInfoView.as_view(), name='product_info'),
    url(r'^search/$', FilterView.as_view(filterset_class=ProductFilter,
                                         template_name='search_product.html', ordering='name'), name='search'),
    url(r'^add_product/$', AddProductView.as_view(), name='add_product'),
    url(r'^edit_product/(?P<pk>[0-9]+)/$', EditProductView.as_view(), name='edit_product'),
    url(r'^delete_product/(?P<pk>[0-9]+)/$', DeleteProductView.as_view(), name='delete_product'),

]