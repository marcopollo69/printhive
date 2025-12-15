from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    path('inquiry/submit/', views.submit_inquiry, name='submit_inquiry'),
    path('inquiry/success/', views.inquiry_success, name='inquiry_success'),
    path('products/', views.products, name='products'),
    path('api/calculate-price/', views.calculate_price, name='calculate_price'),
]
