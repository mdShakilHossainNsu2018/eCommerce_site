from django.urls import path
from .views import ProductList, ProductDetailView

app_name = 'products'
urlpatterns = [
    path('', ProductList.as_view(), name='lists'),
    path('<slug:slug>', ProductDetailView.as_view(), name='details'),
]