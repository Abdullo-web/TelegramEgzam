from django.shortcuts import render
from rest_framework import generics ,status
from rest_framework.permissions import IsAuthenticated
from .models import Channel,ChannelMember,Post
from .serializers import ChannelSerializer,PostSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from django.shortcuts import get_object_or_404

class ChannelListCreateView(generics.ListCreateAPIView):
    serializer_class = ChannelSerializer
    
    
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    
    def get_queryset(self):
        return Channel.objects.filter(
            type='public'
        ).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        
class ChannelDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChannelSerializer
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Channel.objects.all()

    def get_object(self):
        channel = super().get_object()

        if channel.type == 'private':
            user = self.request.user

            if not user.is_authenticated:
                from rest_framework.exceptions import NotFound
                raise NotFound('Канал не найден.')

            is_owner = channel.owner_id == user.id

            is_member = ChannelMember.objects.filter(
                channel=channel,
                user=user
            ).exists()

            if not is_owner and not is_member:
                from rest_framework.exceptions import NotFound
                raise NotFound('Канал не найден.')

        return channel


# .dvsdfvfdv
class ChannelFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, channel_id):
        channel = generics.get_object_or_404(
            Channel, id=channel_id
        )

        if channel.type == 'private':
            is_member = ChannelMember.objects.filter(
                channel=channel,
                user=request.user
            ).exists()

            if channel.owner != request.user and not is_member:
                raise NotFound('Канал не найден.')

        if ChannelMember.objects.filter(
            channel=channel,
            user=request.user
        ).exists():
            return Response(
                {'detail': 'Вы уже подписаны на этот канал.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ChannelMember.objects.create(
            channel=channel,
            user=request.user
        )

        return Response(
            {'detail': 'Вы подписались на канал.'},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, channel_id):
        membership = ChannelMember.objects.filter(
            channel_id=channel_id,
            user=request.user
        ).first()

        if membership is None:
            return Response(
                {'detail': 'Вы не подписаны на этот канал.'},
                status=status.HTTP_404_NOT_FOUND
            )

        membership.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowingListView(generics.ListAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Channel.objects.filter(
            members__user=self.request.user
        ).order_by('-id')


class IsFollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, channel_id):
        is_following = ChannelMember.objects.filter(
            channel_id=channel_id,
            user=request.user
        ).exists()

        return Response({
            'channel_id': channel_id,
            'is_following': is_following
        })
        
        
class ChannelPostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_channel(self):
        channel = get_object_or_404(
            Channel,
            id=self.kwargs['channel_id']
        )

        user = self.request.user

        if channel.type == 'private':
            if not user.is_authenticated:
                raise NotFound('Канал не найден.')

            is_member = ChannelMember.objects.filter(
                channel=channel,
                user=user
            ).exists()

            if channel.owner != user and not is_member:
                raise NotFound('Канал не найден.')

        return channel

    def get_queryset(self):
        channel = self.get_channel()

        return Post.objects.filter(
            channel=channel
        ).order_by('-cr_at')

    def create(self, request, *args, **kwargs):
        channel = self.get_channel()

        if channel.owner != request.user:
            raise PermissionDenied(
                'Только владелец может публиковать в канале.'
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        channel = self.get_channel()
        serializer.save(channel=channel)
        
        
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Post.objects.select_related(
            'channel',
            'channel__owner'
        )

    def get_object(self):
        post = super().get_object()
        channel = post.channel
        user = self.request.user

        if channel.type == 'private':
            if not user.is_authenticated:
                raise NotFound('Публикация не найдена.')

            is_member = ChannelMember.objects.filter(
                channel=channel,
                user=user
            ).exists()

            if channel.owner != user and not is_member:
                raise NotFound('Публикация не найдена.')

        if self.request.method in ['PATCH', 'DELETE']:
            if not user.is_authenticated or channel.owner != user:
                raise PermissionDenied(
                    'Только владелец канала может изменить публикацию.'
                )

        return post