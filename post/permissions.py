from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user
    
class IsReqruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_authenticated
    

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_authenticated and request.user.is_superuser