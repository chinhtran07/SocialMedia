from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user == obj.user


class IsCommentAuthorOrPostAuthor(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        # Allow the author of the comment or the author of the post to delete the comment
        return (self.has_permission(request, view) and
                (request.user == obj.user or request.user == obj.post.user))


class IsOwnerOfMessage(permissions.IsAuthenticated):
    """
    Custom permission to only allow owners of a message to view it.
    """

    def has_permission(self, request, view):
        sender_id = request.query_params.get('sender_id')
        receiver_id = request.query_params.get('receiver_id')

        # Check if the sender and receiver IDs are present in the request
        if sender_id and receiver_id:
            return request.user.id == int(sender_id) or request.user.id == int(receiver_id)
        return False
