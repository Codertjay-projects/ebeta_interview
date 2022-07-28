from django.urls import path

from store.views import StoreViewSet, StoreProducts
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', StoreViewSet, basename='store')
urlpatterns = router.urls
urlpatterns += [
    path('store_products/<str:store_slug>/',StoreProducts.as_view(),name='store_products')
]