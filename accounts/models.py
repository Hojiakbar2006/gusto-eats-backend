from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
import random
from datetime import timedelta
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    email = models.EmailField(
        max_length=255, verbose_name=_("Email Address"), unique=True)
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    phone_number = models.CharField(
        max_length=13, verbose_name=_("Phone Number"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry_time = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def generate_otp(self):
        otp_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
        self.otp_code = otp_code
        self.otp_expiry_time = timezone.now() + timedelta(minutes=3)
        self.save()
        return otp_code

    def verify_otp(self, entered_otp):
        if self.otp_code == entered_otp and self.otp_expiry_time > timezone.now():
            self.otp_code = None
            self.otp_expiry_time = None
            self.save()
            return True
        return False
