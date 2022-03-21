
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from payments.models import Payment
from .models import *
from .utils import cookieCart, cartData,  guestOrder
from django.contrib import messages
import datetime
from django.conf import settings
from payments.models import *


import json

def home(request):


    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']


    products = Product.objects.all()
    context= {
        'products': products,
        'items': items, 
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/main.html', context)

def store(request):

    products = Product.objects.all()

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context= {
        'products': products,
        'items': items, 
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/store.html', context)

def cart(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']


    context= {
        'items': items, 
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'store/cart.html', context)

def checkout(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']


    context= {
        'items': items, 
        'order': order,
        'cartItems': cartItems,

    }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('productId', productId)
    print('action', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    

    return JsonResponse('Item added', safe=False)

    
def detail(request, slug):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    product = get_object_or_404(Product, slug=slug)

    context= {
        "product":product,
        
    }
    return render(request, 'store/detail.html', context)

def delete(request, orderitem_id):

    order_item = get_object_or_404(OrderItem, id=orderitem_id)
    order_item.delete()
    return redirect('cart')

def processOrder(request):

	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)
