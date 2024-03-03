from django.utils.text import slugify
from rest_framework.response import Response
from accounts.models import User
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.views import APIView
from products.models import Feedback, Order, Category, Product, OrderItem
from rest_framework import status
from products.serializers import FeedbackSerializer


class FeedbackAPIView(APIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        return super().get_permissions()

    def get(self, request):
        feedback_objects = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback_objects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        product_count = Product.objects.count()
        order_count = Order.objects.count()
        order_item_count = OrderItem.objects.count()
        category_count = Category.objects.count()
        staff_user_count = User.objects.filter(is_staff=True).count()
        customer_user_count = User.objects.filter(is_staff=False).count()

        data = [
            {'entity': 'Product', 'count': product_count},
            {'entity': 'Order', 'count': order_count},
            {'entity': 'Order Item', 'count': order_item_count},
            {'entity': 'Category', 'count': category_count},
            {'entity': 'Staff User', 'count': staff_user_count},
            {'entity': 'Customer User', 'count': customer_user_count},
        ]

        for item in data:
            item['route_path'] = slugify(item['entity'])

        return Response(data)
