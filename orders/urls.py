from django.urls import path

from orders.views import AddOrRemoveProductFromCartAPIView, CheckoutAPIView, UserOrderAPIView, UserOrderHistory, \
    UpdateOrderState

urlpatterns = [
    path('user_order/', UserOrderAPIView.as_view(), name='user_order'),
    path('user_order_history/', UserOrderHistory.as_view(), name='user_order_history'),

    path('add_or_remove/', AddOrRemoveProductFromCartAPIView.as_view(), name='add_or_remove'),
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('update_order_state/<str:order_ref>/', UpdateOrderState.as_view(), name='checkout'),
]
