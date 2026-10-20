from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Group, GroupMember, GroupMessage
from .serializers import *

User = get_user_model()


class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Group.objects.filter(
            members__user=self.request.user
        ).distinct().order_by('-id')

    def perform_create(self, serializer):
        group = serializer.save(owner=self.request.user)

        GroupMember.objects.create(
            user=self.request.user,
            group=group,
            role='owner'
        )



class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Group.objects.filter(
            members__user=self.request.user
        ).distinct()

    def perform_update(self, serializer):
        group = self.get_object()

        membership = get_object_or_404(
            GroupMember,
            group=group,
            user=self.request.user
        )

        if membership.role not in ['owner', 'admin']:
            raise PermissionDenied(
                'Изменять группу может владелец или администратор.'
            )

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        group = self.get_object()

        if group.owner_id != request.user.id:
            raise PermissionDenied(
                'Удалить группу может только владелец.'
            )

        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class GroupMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_group(self):
        return get_object_or_404(
            Group,
            pk=self.kwargs['group_id']
        )

    def check_membership(self, group):
        return GroupMember.objects.filter(
            group=group,
            user=self.request.user
        ).first()

    def get_queryset(self):
        group = self.get_group()
        membership = self.check_membership(group)

        if membership is None:
            raise PermissionDenied(
                'Просматривать участников могут только участники группы.'
            )

        return GroupMember.objects.filter(
            group=group
        ).select_related('user')

    def create(self, request, *args, **kwargs):
        group = self.get_group()
        membership = self.check_membership(group)

        if membership is None or membership.role not in ['owner', 'admin']:
            raise PermissionDenied(
                'Добавлять участников может владелец или администратор.'
            )

        user_id = request.data.get('user')

        if not user_id:
            return Response(
                {'error': 'Укажи user.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, pk=user_id)

        if GroupMember.objects.filter(group=group, user=user).exists():
            return Response(
                {'error': 'Пользователь уже состоит в группе.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        member = GroupMember.objects.create(
            user=user,
            group=group,
            role='member'
        )

        return Response(
            GroupMemberSerializer(member).data,
            status=status.HTTP_201_CREATED
        )



class GroupMemberDetailView(generics.UpdateAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'head', 'options']

    def get_queryset(self):
        return GroupMember.objects.filter(
            group_id=self.kwargs['group_id']
        )

    def partial_update(self, request, *args, **kwargs):
        group = get_object_or_404(
            Group,
            pk=self.kwargs['group_id']
        )

        if group.owner_id != request.user.id:
            raise PermissionDenied(
                'Изменять роли может только владелец группы.'
            )

        member = self.get_object()

        if member.user_id == group.owner_id:
            return Response(
                {'error': 'Нельзя изменить роль владельца.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        role = request.data.get('role')

        if role not in ['admin', 'member']:
            return Response(
                {'error': 'Роль должна быть admin или member.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        member.role = role
        member.save()

        return Response(GroupMemberSerializer(member).data)




class LeaveGroupView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        group_id = self.kwargs['group_id']

        membership = get_object_or_404(GroupMember,group_id=group_id,user=self.request.user)

        return membership

    def destroy(self, request, *args, **kwargs):
        membership = self.get_object()

        if membership.group.owner_id == request.user.id:
            raise PermissionDenied('Владелец не может выйти из группы.')

        membership.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        group = get_object_or_404(
            Group,
            pk=self.kwargs['group_id']
        )

        is_member = GroupMember.objects.filter(
            group=group,
            user=self.request.user
        ).exists()

        if not is_member:
            raise PermissionDenied(
                'Читать сообщения могут только участники группы.'
            )

        return GroupMessage.objects.filter(
            group=group
        ).select_related('user').order_by('cr_at', 'id')

    def perform_create(self, serializer):
        group = get_object_or_404(
            Group,
            pk=self.kwargs['group_id']
        )

        is_member = GroupMember.objects.filter(
            group=group,
            user=self.request.user
        ).exists()

        if not is_member:
            raise PermissionDenied(
                'Отправлять сообщения могут только участники группы.'
            )

        serializer.save(
            user=self.request.user,
            group=group
        )



class GroupMessageDeleteView(generics.DestroyAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroupMessage.objects.filter(
            user=self.request.user
        )