from rest_framework import permissions

class UpdateOwnProfiles(permissions.BasePermission):
    """Allow users to edit theris own profile"""
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit ther own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
class PostOwnStatus(permissions.BasePermission):
    """Allow user to update their own status"""
    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile_id == request.user.id
