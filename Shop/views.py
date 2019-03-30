from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_filters.views import FilterView
from search_listview.list import SearchableListView
from Shop.models import Product
# Create your views here.
from Shop.forms import AddProductForm, ChangeProductForm


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
    permission_required = 'shop.add_product'
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

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission to add product as a Customer.')
        return super(AddProductView, self).handle_no_permission()


class EditProductView(PermissionRequiredMixin, View):
    permission_required = 'shop.change_product'
    template_name = 'change_product.html'
    form_class = ChangeProductForm

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = self.form_class(initial={
            'name': product.name,
            'producer': product.producer,
            'description': product.description,
            'price': product.price,
            'image': product.image,
        })
        return render(request, self.template_name, {'form': form})

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            product.name = form.cleaned_data.get('name')
            product.producer = form.cleaned_data.get('producer')
            product.description = form.cleaned_data.get('description')
            product.price = form.cleaned_data.get('price')
            if form.cleaned_data.get('image') is None:
                product.image = product.image
            else:
                product.image = form.cleaned_data.get('image')
            product.save()
            messages.success(request, 'Product details sucessfully changed !')
            return redirect('/')
        return render(request, self.template_name, {'form': form})

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission to edit product as a Customer.')
        return super(EditProductView, self).handle_no_permission()
