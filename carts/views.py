from django.shortcuts import render, redirect

# Create your views here.
from carts.models import Cart
from products.models import Product


def cart_home(request):

    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request, 'carts/home.html', {'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            # todo show the message to viewers
            print('opps product not exist')
            return redirect('cart:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            request.session['cart_items'] = cart_obj.products.count()
        else:
            cart_obj.products.add(product_obj)
            request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart:home')