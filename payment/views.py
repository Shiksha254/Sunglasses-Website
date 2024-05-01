from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from bii.models import Product

def process_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')

        
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals
        if request.user.is_authenticated:
                user = request.user
                create_order = Order.objects.create(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
                create_order.save()
                create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid )
                create_order.save()
                order_id = create_order.pk
                for product in cart_products:
                    product_id = product.id
                    if product.on_sale:
                        price = product.sale_price
                    else:
                        price = product.price
                        for key, value in quantities.items():
                            if int(key) == product.id:
                                create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                                create_order_item.save()
                messages.success(request, "Order Placed!")
                return redirect("home")
        else:
            create_order = Order.objects.create(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk
            for product in cart_products:
                    product_id = product.id
                    if product.on_sale:
                        price = product.sale_price
                    else:
                        price = product.price
                        for key, value in quantities.items():
                            if int(key) == product.id:
                                create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                                create_order_item.save()
            messages.success(request, "Order Placed!")
            return redirect("home")
    else:
        messages.success(request, "Access Denied")
        return redirect("home")
    

def payment_success(request):
    return render(request, 'payment/payment_success.html')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    # shipping_user = None
    my_shipping = request.POST
    request.session['my_shipping'] = my_shipping

    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            # Handle the case where no shipping address exists for the user
            pass

    shipping_form = ShippingForm(request.POST or None)

    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'shipping_user': shipping_user,
        'shipping_form': shipping_form,
    }

    return render(request, 'payment/checkout.html', context)
     
def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, 'billing_form': billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, 'billing_form': billing_form})
    else:
        messages.success(request, "Access Denied")
        return redirect("home")
