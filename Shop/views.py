from django.shortcuts import render
from django.views import generic, View
from Shop.models import Product
# Create your views here.


class MainPageView(generic.TemplateView):
    template_name = 'index.html'


class ProductsListView(generic.ListView):
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.all().order_by('name')


class ProductInfoView(View):
    template_name = 'product_info.html'

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, self.template_name, {'product': product})

