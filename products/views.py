from django.shortcuts import render
from django.views.generic import ListView, DetailView

from carts.models import Cart
from .models import Product
# Create your views here.


class ProductList(ListView):
    model = Product
    # queryset = Product.objects.all()


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context