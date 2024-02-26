from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    class Role(models.IntegerChoices):
        ALUMNI = 1, "Alumni"
        LECTURER = 2, "Lecturer"
        ADMIN = 3, "Admin"
    email = models.EmailField("email_address", unique=True, null=True)
    role = models.IntegerField(choices=Role.choices, default=Role.ALUMNI)
    avatar = CloudinaryField('avatar', null=True)
    cover_image = CloudinaryField('cover_image', null=True)
    password_changed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.role == User.Role.LECTURER:
            self.set_password(settings.PASSWORD_LECTURER_DEFAULT)
        super().save()


class FriendShip(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_received')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} -> {self.receiver}'


class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_id = models.CharField(max_length=10, unique=True, null=False)

    class Meta:
        unique_together = ('user', 'student_id')

    def __str__(self):
        return f"{self.user}'s Profile"


class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='group_members', related_query_name='group_member')

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class PostBaseModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_blocked = models.BooleanField(default=False)
    shared_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True


class Post(PostBaseModel):
    content = RichTextField(null=True)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')


class Survey(PostBaseModel):
    title = models.TextField()

    def __str__(self):
        return self.title


class Question(BaseModel):
    class Type(models.IntegerChoices):
        TEXT = 1, "Text"
        MULTICHOICE = 2, "MCQ"
    type = models.IntegerField(choices=Type.choices, default=Type.TEXT)
    title = models.CharField(max_length=255, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return self.title


class Choice(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', null=True)


class SurveyResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    response_date = models.DateTimeField(auto_now_add=True)


class QuestionResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField()
    survey_response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE)


class Invitation(PostBaseModel):
    title = models.CharField(max_length=255, null=True)
    content = models.TextField()
    time = models.DateTimeField(null=True)
    place = models.CharField(max_length=255, null=True)
    recipients_users = models.ManyToManyField(User, related_name='recipients_users')
    recipients_groups = models.ManyToManyField(Group, related_name='recipients_groups')

    def __str__(self):
        return self.title


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.TextField()


class Reaction(Interaction):
    class ReactionTypes(models.IntegerChoices):
        LIKE = 1, "Like"
        HAHA = 2, "Haha"
        LOVE = 3, "Love"

    active = models.BooleanField(default=True)
    type = models.IntegerField(choices=ReactionTypes, null=True)

    def __str__(self):
         return self.type.name

    class Meta:
        unique_together = ('user', 'post')


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.content}"

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def create_friend_request_notification(cls, sender, receiver):
        content = f"You have a friend request from {sender.first_name}."
        cls.objects.create(user=receiver, content=content)

    @classmethod
    def create_invitation_notification(cls, invitation):
        for user in invitation.recipients_users.all():
            content = f"You have an invitation: {invitation.title}"
            cls.objects.create(user=user, content=content)

        for group in invitation.recipients_groups.all():
            for user in group.members.all():
                content = f"You have an invitation from {invitation.sender.username}: {invitation.title}"
                cls.objects.create(user=user, content=content)

    @classmethod
    def mark_as_read(cls, notification_ids):
        cls.objects.filter(pk__in=notification_ids).update(is_read=True)

