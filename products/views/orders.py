from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from ..models import Product, Order, OrderItem, ShippingAddress
from ..serializers import OrderSerializer
from django.utils import timezone


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        user = request.user

        if user.is_staff:
            queryset = Order.objects.all()
        elif user.is_authenticated:
            queryset = Order.objects.filter(user=user)
        else:
            queryset = Order.objects.filter(user=None)

        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        if not user:
            return Response({'error': 'User '}, status=status.HTTP_400_BAD_REQUEST)

        if 'orderItems' not in data or not data['orderItems']:
            return Response({'error': 'No Order Items provided'}, status=status.HTTP_400_BAD_REQUEST)

        order_items = data['orderItems']

        order = Order.objects.create(
            user=user,
            paymentMethod=data.get('paymentMethod'),
            name=data.get('name'),
            phone_number=data.get('phone_number'),
            shippingPrice=data.get('shippingPrice') or 0,
            totalPrice=data.get('totalPrice')
        )

        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
        )
        # total_order_price = order.shippingPrice
        for item_data in order_items:
            product_id = item_data.get('product')
            qty = item_data.get('qty')

            if not product_id or not qty:
                return Response({'error': 'Invalid order item data'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': f'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

            if product.countInStock is None or product.countInStock < qty:
                return Response({'detail': f'Insufficient stock for product {product_id}'}, status=status.HTTP_400_BAD_REQUEST)

            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=qty,
            )
            # total_order_price += int(order_item.price)

            product.countInStock -= qty
            product.save()

            # order.totalPrice = total_order_price
            # order.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        # Agar foydalanuvchi admin bo'lsa yoki buyurtma o'ziga tegishli bo'lsa
        if user.is_staff or instance.user == user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

            # Foydalanuvchi buyurtmani o'ziga tegishli emas
        return Response({'detail': 'No order'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def mark_as_paid(self, request, pk=None):
        user = request.user
        order = self.get_object()

        # Foydalanuvchi faqat o'ziga tegishli buyurtmalarini to'lashi mumkin
        if not (request.user.is_staff or (request.user == order.user)):
            return Response({'detail': 'Not authorized to mark as paid'}, status=status.HTTP_400_BAD_REQUEST)

        if order.isPaid:
            return Response({'detail': 'Already paid'}, status=status.HTTP_400_BAD_REQUEST)

        # order.isPaid ni teskari qiymatga o'zgartirish
        order.isPaid = True
        order.paidAt = timezone.now()
        order.save()

        return Response('Order was paid', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def mark_as_delivered(self, request, pk=None):
        order = self.get_object()

        # Agar foydalanuvchi admin bo'lmasa va order.user uningga teng bo'lmasa
        # yoki foydalanuvchi admin bo'lsa, lekin admin order isDelivered sifatida belgilangan bo'lsa
        # mana shu holatda chiqib ketadi
        if not request.user.is_staff or (request.user.is_staff):
            return Response({'detail': 'Not authorized to mark'}, status=status.HTTP_400_BAD_REQUEST)

        if order.isPaid:
            return Response({'detail': 'Already delivered'}, status=status.HTTP_400_BAD_REQUEST)

        # Oldingi qiymatiga teskari bo'lishi
        order.isDelivered = not order.isDelivered
        order.deliveredAt = timezone.now()
        order.save()

        # Xabar va statusni ham o'zgartirish
        message = {"message": 'Order was delivered'} if order.isDelivered else {
            "message": 'Order delivery status was updated'}
        status_code = status.HTTP_200_OK if order.isDelivered else status.HTTP_202_ACCEPTED
        return Response(message, status=status_code)
