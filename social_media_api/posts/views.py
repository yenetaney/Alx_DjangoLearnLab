from django.shortcuts import render, get_object_or_404
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets, permissions, status, generics
from .models import Post, Comment, Like
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from notifications.models import Notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from notifications.utils import create_notification
from rest_framework.decorators import action


# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            create_notification(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )
            return Response({'detail': 'You liked this post.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'You already liked this post.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({'detail': 'You unliked this post.'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        comment = serializer.save(author=self.request.user)
        create_notification(
            recipient=comment.post.author,
            actor=self.request.user,
            verb='commented on your post',
            target=comment.post
    )

class FeedView(APIView):
    def get(self, request):
        user = request.user
        following_users = user.following.all()

        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Prevent duplicate likes
    if Like.objects.filter(user=user, post=post).exists():
        return Response({'detail': 'You have already liked this post.'}, status=400)

    Like.objects.create(user=user, post=post)

    # Create notification
    if post.author != user:  # Avoid notifying self-likes
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb='liked your post',
            content_type=ContentType.objects.get_for_model(Post),
            object_id=post.id
        )

    return Response({'detail': 'Post liked successfully.'}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    like = Like.objects.filter(user=user, post=post).first()
    if not like:
        return Response({'detail': 'You have not liked this post.'}, status=400)

    like.delete()
    return Response({'detail': 'Post unliked successfully.'}, status=200)
