from rest_framework import serializers

from .models import User, AlumniProfile, Post, Comment, FriendShip, Group, Question, Survey, \
    Invitation, Answer, Reaction


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data['password'])
        # student is not confirmed
        user.is_active = False
        user.save()

        return user


class UserDetailSerializer(UserSerializer):
    cover_image = serializers.ImageField()

    class Meta:
        model = UserSerializer.Meta.model
        fields = ['first_name', 'last_name', 'email', 'avatar', 'cover_image', 'role']
        extra_kwargs = {
            'role': {
                'read_only': True
            }
        }


class FriendShipSerializer(serializers.ModelSerializer):
    sender = UserDetailSerializer()
    receiver = UserDetailSerializer()

    class Meta:
        model = FriendShip
        fields = ['id', 'sender', 'receiver']


class AlumniSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AlumniProfile
        fields = ['student_id', 'user']
        extra_kwargs = {
            'student_id': {
                'required': True
            }
        }


class PostSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Post
        fields = ['id', 'content', 'comment_blocked', 'created_date', 'updated_date', 'user']


class PostDetailSerializer(PostSerializer):

    def get_reacted(self, post):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return post.reaction_set.filter(active=True).exists()

    class Meta:
        model = PostSerializer.Meta.model
        fields = PostSerializer.Meta.fields + ['reacted']


class CommentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    members = UserDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'members']


class InvitationSerializer(serializers.ModelSerializer):
    recipients_users = UserDetailSerializer(many=True, read_only=True)
    recipients_groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Invitation
        fields = '__all__'


class ReactionSerializer(serializers.ModelSerializer):
    User = UserDetailSerializer()

    class Meta:
        model = Reaction
        fields = '__all__'
