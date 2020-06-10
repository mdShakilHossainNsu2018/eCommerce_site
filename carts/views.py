from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from carts.models import Cart
from orders.models import Order
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


def checkout_view(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    else:
        order_obj, new_order = Order.objects.get_or_create(cart=cart_obj)

    user = request.user
    login_form = LoginForm()
    guestForm = GuestForm()
    billing_profile = None
    if user.is_authenticated:
        billing_profile = BillingProfile.objects.get_or_create(user=user, email=user.email)

    context = {'object': order_obj,
               'billing_profile': billing_profile,
               'login_form': login_form,
               }
    return render(request, 'carts/checkout.html', context)
