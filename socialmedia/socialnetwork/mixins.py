from .models import FriendShip, User
import string, random


class FriendRequestMixin:

    def create_friend_request(self, sender, receiver):
        return FriendShip.objects.create(sender=sender, receiver=receiver)


class ForgetPasswordMixin:
    def change_random_password(self, instance, email):
        length = 12
        characters = string.ascii_letters + string.digits + string.punctuation

        lowercase = random.choice(string.ascii_lowercase)
        uppercase = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        punctuation = random.choice(string.punctuation)

        remaining_characters = ''.join(random.choice(characters) for _ in range(length - 4))

        password_list = list(lowercase + uppercase + digit + punctuation + remaining_characters)
        random.shuffle(password_list)

        password = ''.join(password_list)

        instance.set_password(password)
        instance.save()

        return password
