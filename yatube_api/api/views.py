from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, NotFound

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

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post_id=post_id)
        if queryset != []:
            return Comment.objects.filter(post_id=post_id)
        else:
            raise NotFound('Комментарии не найдены.')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class CommentDetail(
    AuthorPremissionMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
