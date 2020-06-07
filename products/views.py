from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product
# Create your views here.


class ProductList(ListView):
    model = Product
    # queryset = Product.objects.all()


class ProductDetailView(DetailView):
    model = Product