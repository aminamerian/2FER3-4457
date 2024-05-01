from rest_framework import permissions


class AdvertisementPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            return bool(request.user and request.user.is_authenticated)
        return True

    def has_object_permission(self, request, view, obj):
        # Only creator of the advertisement can update or delete it.
        if request.method in ("PUT", "PATCH", "DELETE"):
            return request.user == obj.created_by
        return True
