from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_filters.views import FilterView
from search_listview.list import SearchableListView
from Shop.models import Product
# Create your views here.
from Shop.forms import AddProductForm


class MainPageView(generic.TemplateView):
    template_name = 'base.html'


class ProductsListView(SearchableListView):
    template_name = 'product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.all().order_by('name')
    paginate_by = 15
    model = Product


class ProductInfoView(View):
    template_name = 'product_info.html'

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, self.template_name, {'product': product})


class AddProductView(PermissionRequiredMixin, View):
    permission_required = ('shop.add_product', 'shop.delete_product', 'shop.change_product')
    template_name = 'add_product.html'
    form_class = AddProductForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.success(request, 'New product sucessfully added !')
            return redirect('/')
        return render(request, self.template_name, {'form': form})

