import json
from .models import *

def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = { 'get_cart_total':0, 'get_cart_item': 0, 'shipping': False }
    cartItems = order['get_cart_item']

    for i in cart:

        try:

            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order[ 'get_cart_total'] += total
            order[ 'get_cart_item'] += cart[i]['quantity']

            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageUrl':product.imageUrl

                },
                'quantity': cart[i]['quantity'],
                'get_total': total, 
            
            }
            items.append(item)
        except:
            pass
    return{'items': items, 
        'order': order,
        'cartItems': cartItems,}


def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    return{'items': items, 
        'order': order,
        'cartItems': cartItems,}