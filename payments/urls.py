from django.urls import path
from . import views

urlpatterns = [
    path('page/', views.HomePageView.as_view(), name='homepage'),
]
