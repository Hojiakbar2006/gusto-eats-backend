from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Product, Order, OrderItem, ShippingAddress
from ..serializers import OrderSerializer
import requests
from django.shortcuts import get_object_or_404
from django.conf import settings


def send_telegram_message(message):
    for i in settings.ADMINS_ID:
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={i}&text={message}")
        


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if not user:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)

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

        shipping_address = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
        )

        for item_data in order_items:
            product_id = item_data.get('product')
            qty = item_data.get('qty')

            if not product_id or not qty:
                return Response({'error': 'Invalid order item data'}, status=status.HTTP_400_BAD_REQUEST)

            product = get_object_or_404(Product, id=product_id)

            if product.countInStock is None or product.countInStock < qty:
                return Response({'detail': f'Insufficient stock for product {product_id}'}, status=status.HTTP_400_BAD_REQUEST)

            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=qty,
            )

            product.countInStock -= qty
            product.save()

        # Send Telegram notification to admin
        order_details = f"New order received:\n\nName: {order.name}\nPhone Number: {
            order.phone_number}\nAddress: {shipping_address.address}\n\nProducts \n>>>\n"
        for order_item in order.orderitem_set.all():
            order_details += f"Product ID: {order_item.product.id} \nProduct Name: {
                order_item.product.name} \nQuantity: {order_item.qty}\n\n"
        order_details += f"Total Price: {order.totalPrice}"
        send_telegram_message(order_details)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
