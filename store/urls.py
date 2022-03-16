from django.urls import path
from . import views

urlpatterns = [

     path('', views.home, name='home'),
     path('store/', views.store, name='store'),
     path('cart/', views.cart, name='cart'),
     path('checkout/', views.checkout, name='checkout'),
     path('update_item/', views.updateItem, name='update_item'),
     path('process_order/', views.processOrder, name='process_order'),
     path('product/detail/<str:id>', views.detail, name='detail'),
     path('order/product/delete/<str:orderitem_id>', views.delete, name='delete'),
]
