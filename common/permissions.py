from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModerator(BasePermission):
    def has_permission(self, request, view): # type: ignore
        return bool(request.user.is_authenticated and request.user.is_staff)
    
    def has_object_permission(self, request, view, obj):
        return obj.director == request.user
