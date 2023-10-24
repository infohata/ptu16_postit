from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'body', 'username', 'user_id', 'created_at']
