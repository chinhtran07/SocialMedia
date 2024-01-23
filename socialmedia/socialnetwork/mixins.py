from .models import FriendShip


class FriendRequestMixin:

    def create_friend_request(self, sender, receiver):
        return FriendShip.objects.create(sender=sender, receiver=receiver)
