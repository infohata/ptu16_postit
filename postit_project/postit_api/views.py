from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions
from rest_framework.validators import ValidationError
from . import models, serializers


class PostList(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, *args, **kwargs):
        post = models.Post.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user,
        )
        if post.exists():
            return self.destroy(self.request, *args, **kwargs)
        else:
            raise ValidationError(_('You can only delete your own posts'))

    def put(self, *args, **kwargs):
        post = models.Post.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user,
        )
        if post.exists():
            return self.update(self.request, *args, **kwargs)
        else:
            raise ValidationError(_('You can only update your own posts'))


class CommentList(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return models.Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, *args, **kwargs):
        post = models.Comment.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user,
        )
        if post.exists():
            return self.destroy(self.request, *args, **kwargs)
        else:
            raise ValidationError(_('You can only delete your own comments'))

    def put(self, *args, **kwargs):
        post = models.Comment.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user,
        )
        if post.exists():
            return self.update(self.request, *args, **kwargs)
        else:
            raise ValidationError(_('You can only update your own comments'))
