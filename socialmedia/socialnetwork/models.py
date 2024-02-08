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


class Survey(PostBaseModel):
    content = models.TextField()
    # form_id = models.CharField(max_length=20, null=True)


class Question(BaseModel):
    content = models.TextField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")


class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questions', null=True)


class Invitation(PostBaseModel):
    content = models.TextField()
    recipients_users = models.ManyToManyField(User, related_name='notifications_received')
    recipients_groups = models.ManyToManyField(Group, related_name='notifications_received')


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