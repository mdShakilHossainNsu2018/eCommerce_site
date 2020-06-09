from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from products.models import Product


class ProductSearchView(ListView):
    template_name = 'search/product_search_list.html'

    model = Product

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(ProductSearchView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):

        query = self.request.GET.get('q', None)

        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()
