from rest_framework import permissions

class IsOwnerOrManagerToDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return request.user == obj.created_by or request.user.manager_profile.exists()

        return request.user == obj.created_by

class IsAuthenticatedToCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST' and request.user.is_authenticated
