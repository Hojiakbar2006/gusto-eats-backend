from datetime import datetime
from products.serializers import OrderSerializer
from products.models import Product, Order, OrderItem, ShippingAddress
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from products.permissions import IsOwner
from ..models import Product, Order, OrderItem, ShippingAddress
from accounts.models import ChatId
from ..serializers import OrderSerializer
import requests
from django.shortcuts import get_object_or_404
from django.conf import settings


def send_telegram_message(message):
    chat_ids = ChatId.objects.values_list('chat_id', flat=True)
    if not chat_ids:
        return
    for chat_id in chat_ids:
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={message}")


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>ADD ORDER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data

    if 'orderItems' not in data or not data['orderItems']:
        return Response({'detail': 'No Order Items provided'}, status=status.HTTP_400_BAD_REQUEST)

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

    try:
        send_telegram_message(order_details)
    except Exception as e:
        return Response({"detail": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message": "Order added  succeccfully"}, status=status.HTTP_201_CREATED)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>ADD ORDER


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>MY ORDER
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>GET MY ORDER


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>GET ORDER
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>GET ORDER


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>GET ORDER BY ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user

    try:
        order = Order.objects.get(id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this order'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist', }, status=status.HTTP_400_BAD_REQUEST)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>UPDATE ORDER PAY
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()

    return Response('Order was paid')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>UPDATE ORDER PAY


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>UPDATE ORDER DELIVERY
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    order = Order.objects.get(id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response('Order was delivered')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>UPDATE ORDER DELIVERY
