from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = f"{obj.first_name} {obj.last_name}"
        if name == '':
            name = obj.email
        return name


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'phone_number', 'password', 'password2', 'isAdmin']

    def get_isAdmin(self, obj):
        return obj.is_staff

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password'),
            phone_number=validated_data.get('phone_number')
        )


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    is_admin = serializers.BooleanField(
        read_only=True)  # Yangi qo'shilgan xususiyat

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name',
                  'access_token', 'refresh_token', 'is_admin']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed(
                "Ma'lumotlar mos kelmadi")
        attrs['is_admin'] = user.is_staff

        tokens = user.tokens()
        return {
            'email': user.email,
            'full_name': user.get_full_name,
            "access_token": str(tokens.get('access')),
            "refresh_token": str(tokens.get('refresh')),
            "is_admin": user.is_staff
        }


class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise AuthenticationFailed(
                'Token is expired or invalid', code='bad_token')
