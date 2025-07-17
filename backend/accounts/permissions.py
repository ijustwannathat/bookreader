from rest_framework import permissions



class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.added_by == request.user or request.user == request.user.is_staff
