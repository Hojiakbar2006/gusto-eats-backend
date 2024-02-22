from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'chat_id', ChatIdViewSet,  basename='chat_id')


urlpatterns = [
    path('', include(router.urls)),
    path("login/", login_user, name="login"),
    path("register/", register_user, name="register"),
    path("profile/", get_user_profile, name="get_user_profile"),
    path("profile-update/", update_user_profile, name="update_user_profile"),
    path("send-otp/", send_otp, name="send_otp"),
    path("reset-password/", reset_password, name="reset_password"),
    path("logout/", logout_user, name="logout"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # //for admins
    path("users/", get_users, name="get_users"),
    path("users_staff/", get_users_staff, name="get_users_staff"),
]
