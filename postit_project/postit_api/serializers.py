from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'body', 'image', 'username', 'user_id', 
                  'created_at', 'comment_count', 'comments', 'likes_count']

    def get_comment_count(self, obj):
        return models.Comment.objects.filter(post=obj).count()
    
    def get_likes_count(self, obj):
        return models.PostLike.objects.filter(post=obj).count()


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ['id', 'post', 'body', 'username', 'user_id', 'created_at', 'likes_count']

    def get_likes_count(self, obj):
        return models.CommentLike.objects.filter(comment=obj).count()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostLike
        fields = ['id']


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentLike
        fields = ['id']
