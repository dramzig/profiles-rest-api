from rest_framework import permissions

class UpdateOwnProfiles(permissions.BasePermission):
    """Allow users to edit theris own profile"""
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit ther own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
