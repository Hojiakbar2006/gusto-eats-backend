from django.urls import path, include
from .views import products, orders, misk
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', products.ProductViewSet)
router.register(r'categories', products.CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('orders/add/', orders.add_order_items, name='add_order_items'),
    path('myorders/', orders.getMyOrders, name='get_my_orders'),
    path('orders/', orders.getOrders, name='get_orders'),
    path('api/orders/<int:pk>/paid/', orders.updateOrderToPaid,
         name='update_order_to_paid'),
    path('api/orders/<int:pk>/delivered/', orders.updateOrderToDelivered,
         name='update_order_to_delivered'),
    path('api/orders/<int:pk>/', orders.getOrderById, name='get_order_by_id'),




    path('admin/stats/', misk.AdminStatsView.as_view(), name='admin-stats'),
    path('feedback/', misk.FeedbackAPIView.as_view())
]
