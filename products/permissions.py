from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Foydalanuvchiga faqat o'qish ruxsati
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Faqat adminlar uchun ruxsat
        return request.user and request.user.is_staff
    

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user
