from django.urls import path, include
from .views import products
from .views.orders import OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', products.ProductViewSet)
router.register(r'categories', products.CategoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'feedback', products.FeedbackViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
