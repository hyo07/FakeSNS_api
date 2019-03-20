from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Write permissions are only allowed to the author of a post
        return obj.author == request.user


class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Write permissions are only allowed to the author of a post
        return obj.user == request.user
