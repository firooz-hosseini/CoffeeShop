from rest_framework.permissions import BasePermission


class IsOwnerOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    

class IsAuthenticatedWithMessage(BasePermission):
    message = "You must be logged in to comment."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)