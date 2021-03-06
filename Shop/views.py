from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.conf import settings
import datetime

from search_listview.list import SearchableListView
from Shop.models import Product, OrderItem
from Shop.forms import AddProductForm, CartAddProductForm, OrderCreateForm
from Shop.cart import Cart
from Shop.utils import render_to_pdf


# Create your views here.


class MainPageView(generic.TemplateView):
    template_name = 'index.html'


class ProductsListView(SearchableListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.all().order_by('name')
    paginate_by = 15
    model = Product


class ProductInfoView(View):
    template_name = 'products/product_info.html'
    form_class = CartAddProductForm

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = self.form_class
        return render(request, self.template_name, {'product': product, 'form': form})


class AddProductView(PermissionRequiredMixin, View):
    permission_required = 'Shop.add_product'
    template_name = 'products/add_product.html'
    form_class = AddProductForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.success(request, 'New product successfully added !')
            return redirect('/')
        return render(request, self.template_name, {'form': form})

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission to add product as a Customer.')
        return super(AddProductView, self).handle_no_permission()


class EditProductView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'Shop.change_product'
    model = Product
    fields = ['name', 'producer', 'description', 'price', 'image']
    template_name = 'products/change_product.html'
    success_url = reverse_lazy('Shop:products_list')

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission to edit product as a Customer.')
        return super(EditProductView, self).handle_no_permission()


class DeleteProductView(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'Shop.delete_product'
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('Shop:products_list')

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission to delete product as a Customer.')
        return super(DeleteProductView, self).handle_no_permission()


@require_POST
@login_required
@permission_required('Shop.add_order')
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('Shop:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('Shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                                                                    'quantity': item['quantity'],
                                                                    'update': True,
                                                                })
    return render(request, 'orders/cart_detail.html', {'cart': cart})


class CreateOrderView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'Shop.add_order'
    template_name_get = 'orders/order.html'
    template_name_post = 'orders/order_created.html'
    form_class = OrderCreateForm

    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                                                                        'quantity': item['quantity'],
                                                                        'update': True,
                                                                    })
        form = self.form_class(initial={
            'payment_deadline': datetime.date.today() + datetime.timedelta(days=5),
            'value': cart.get_total_price(),
        })
        return render(request, self.template_name_get, {'form': form, 'cart': cart})

    def post(self, request):
        cart = Cart(request)
        form = self.form_class(request.POST, request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.client_id = request.user.id
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])
            cart.clear()

            current_site = get_current_site(request)
            mail_subject = 'Order confirmation'
            message = render_to_string('orders/confirmation_email.html', {
                                                                    'user': request.user,
                                                                    'domain': current_site.domain,
                                                                })
            to_email = request.user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            pdf_context = {
                'order': order.id,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'total_price': form.cleaned_data['value'],
                'date': order.date,
                'deadline': order.payment_deadline,
                'cart': cart,
                'seller': settings.SELLER_ADRESS,
            }
            pdf = render_to_pdf('orders/invoice.html', pdf_context)
            email.attach('invoice{}.pdf'.format(order.id), pdf.getvalue(), 'Shop/pdf')
            email.send()
            return render(request, self.template_name_post, {'order': order})
