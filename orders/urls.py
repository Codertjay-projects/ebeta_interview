from django.urls import path

from orders.views import AddOrRemoveProductFromCartAPIView, CheckoutAPIView, UserOrderAPIView, UserOrderHistory, \
    UpdateOrderState, AdminUpdateOrderState, AdminListOrdersAPIView, AdminRetrieveDestroyAPIView

urlpatterns = [
    path('user_order/', UserOrderAPIView.as_view(), name='user_order'),
    path('user_order_history/', UserOrderHistory.as_view(), name='user_order_history'),

    path('add_or_remove/', AddOrRemoveProductFromCartAPIView.as_view(), name='add_or_remove'),
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('update_order_state/<str:ref_code>/', UpdateOrderState.as_view(), name='update_order'),
    # admin update order

    path('admin_list_orders/', AdminListOrdersAPIView.as_view(), name='admin_list_orders'),
    path('admin_retrieve_destroy/<str:ref_code>/', AdminRetrieveDestroyAPIView.as_view(),
         name='admin_retrieve_destroy'),
    path('admin_update_order_state/<str:ref_code>/', AdminUpdateOrderState.as_view(), name='admin_update_order_state'),
]
