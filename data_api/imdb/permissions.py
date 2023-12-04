from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
import jwt
import os
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
    

class IsJWTAuthenticated(permissions.BasePermission):
    """
    Custom permission to check JWT authentication and permissions.
    """

    def has_permission(self, request, view):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()

        if not auth or auth[0].lower() != 'bearer' or len(auth) != 2:
            return False

        token = auth[1]
        try:
            payload = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=['HS256'])
            # Check permissions in the payload, for example:
            # Assuming the payload has a 'permissions' key
            # required_permissions = [permissions.IsAuthenticated]
            print(payload.get('permissions', []))
            # if not set(required_permissions).issubset(set(payload.get('permissions', []))):
            #     return False


        except jwt.ExpiredSignatureError:
            raise PermissionDenied('Token is expired.')
        except jwt.InvalidTokenError:
            raise PermissionDenied('Invalid token.')

        return True