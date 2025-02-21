from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class AuthorPremissionMixin:

    def perform_update(self, serializer):
        if serializer.instance.author.username != self.request.user.username:
            raise PermissionDenied('Изменение чужого контента запрещено.')
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author.username != self.request.user.username:
            raise PermissionDenied('Удаление чужого контента запрещено.')
        return super().perform_destroy(instance)


class PostViewSet(AuthorPremissionMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class CommentDetail(
    AuthorPremissionMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
