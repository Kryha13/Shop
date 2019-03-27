from django.shortcuts import render
from django.views import generic, View
from search_listview.list import SearchableListView
from Shop.models import Product
# Create your views here.


class MainPageView(generic.TemplateView):
    template_name = 'index.html'


class ProductsListView(SearchableListView):
    template_name = 'product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.all().order_by('name')
    paginate_by = 20
    model = Product
    searchable_fields = ['name']
    specifications = {
        "name": "__icontains"
    }


class ProductInfoView(View):
    template_name = 'product_info.html'

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, self.template_name, {'product': product})

