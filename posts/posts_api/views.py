import re
from django.http import request
from posts.posts_api.serializers import PostSerializer
from posts.models import Post, Comment, Like
from rest_framework import viewsets
from .serializers import CommentSerializer, PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'

    @action(detail=True, methods=["GET"])
    def comments(self, request, id=None):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['POST'])
    def choice(self, request, id=None):
        post = self.get_object()
        data = request.data
        data['post'] = post.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)