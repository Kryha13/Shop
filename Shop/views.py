from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.http import require_POST
from search_listview.list import SearchableListView
from Shop.models import Product
from Shop.forms import AddProductForm, OrderForm, CartAddProductForm
from Shop.cart import Cart

# Create your views here.


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
        cart_product_form = CartAddProductForm()
        return render(request, self.template_name, {'product': product, 'cart_product_form': cart_product_form})


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


class EditProductView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'shop.change_product'
    model = Product
    fields = ['name', 'producer', 'description', 'price', 'image']
    template_name = 'change_product.html'
    success_url = reverse_lazy('Shop:products_list')

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission to edit product as a Customer.')
        return super(EditProductView, self).handle_no_permission()


class DeleteProductView(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'shop.delete_product'
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('Shop:products_list')

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission to delete product as a Customer.')
        return super(DeleteProductView, self).handle_no_permission()


class OrderView(PermissionRequiredMixin, View):
    permission_required = ('shop.add_order', 'shop.change_order', 'shop.delete_order')
    template_name = 'order.html'
    form_class = OrderForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})


@require_POST
@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('Shop:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('Shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart_detail.html', {'cart': cart})

