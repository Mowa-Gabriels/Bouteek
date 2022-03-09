from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
import json
from .utils import cookieCart, cartData
# Create your views here.

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

    
def detail(request, product_id):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    product = get_object_or_404(Product, id=product_id)

    context= {
        "product":product,
        
    }
    return render(request, 'store/detail.html', context)