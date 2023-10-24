from rest_framework import generics
from . import models, serializers


class PostList(generics.ListAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
