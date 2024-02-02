from accounts.models import User
from config import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import *
from .serializers import *


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    users = get_user_model().objects.filter(is_staff=False)
    if not users:
        return Response({'message': 'No Users'})
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users_staff(request):
    users = get_user_model().objects.filter(is_staff=True)
    if not users:
        return Response({'message': 'No staff users'})
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = UserProfileSerializer(
        user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user_data = serializer.data
        return Response({
            'data': user_data,
            'message': "Muvafaqiyalit ro'yxatdan o'tdingiz",
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(
        data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_otp(request):
    email = request.data.get('email')

    if not email:
        return Response({"detail": "Email to'ldirilmagan"}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(get_user_model(), email=email)
    otp_code = user.generate_otp()
    user.save()

    send_mail(
        "Parol yangilash",
        f"Parolingizni yangilash uchun otp code: {otp_code}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    return Response({"message": "emailingizga otp code jo'natildi"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password(request):
    email = request.data.get('email')
    otp_code = request.data.get('otp_code')
    new_password = request.data.get('new_password')
    new_password2 = request.data.get('new_password2')

    if not email:
        return Response({"detail": "Email to'dirilmagan"}, status=status.HTTP_400_BAD_REQUEST)

    if not otp_code:
        return Response({"detail": "OTP code topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if not new_password:
        return Response({"detail": "Yangi parol to'dirilmagan"}, status=status.HTTP_400_BAD_REQUEST)

    if not new_password2:
        return Response({"detail": "Yangi parol to'dirilmagan"}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != new_password2:
        return Response({"detail": "Parollar mos emas"}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(get_user_model(), email=email)

    if not user.verify_otp(otp_code):
        return Response({"detail": "Yaroqsiz otp code"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Parol muvafaqiyatli yangilandi"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    serializer = LogoutUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({"message": "Muvafaqiyatli chiqish"}, status=status.HTTP_204_NO_CONTENT)
