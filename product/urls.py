from django.urls import path

from product.views import ProductListAPIView, ProductCreateAPIView, ProductRetUpdateDestroyAPIView

app_name = 'product'
urlpatterns = [
    path('', ProductListAPIView.as_view(), name='products'),
    path('product_create/', ProductCreateAPIView.as_view(), name='products'),
    path('<str:slug>/', ProductRetUpdateDestroyAPIView.as_view(), name='products'),
]
