from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user == obj


class IsCommentAuthorOrPostAuthor(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        # Allow the author of the comment or the author of the post to delete the comment
        return (self.has_permission(request, view) and
                (request.user == obj.author or request.user == obj.post.author))