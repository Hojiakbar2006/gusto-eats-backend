from django.urls import path, include
from .views import products, orders, misk
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', products.ProductViewSet)
router.register(r'categories', products.CategoryViewSet)
router.register(r'orders', orders.OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/stats/', misk.AdminStatsView.as_view(), name='admin-stats'),
    path('feedback/', misk.FeedbackAPIView.as_view())
]
