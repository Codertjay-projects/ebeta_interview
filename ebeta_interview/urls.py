from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/stores/', include('store.urls')),
    path('api/v1/products/', include('product.urls')),
    path('api/v1/order/', include('order.urls')),
]

authentication_url_patterns = [
    # registration  from rest-auth
    path('api/v1/auth/registration/', RegisterView.as_view(), name='register'),
    path('api/v1/auth/login/', LoginView.as_view(), name='login'),
]

urlpatterns += authentication_url_patterns
