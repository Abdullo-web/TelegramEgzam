from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import Group, GroupMember, GroupMessage
from .serializers import GroupSerializer, GroupMessageSerializer


class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Group.objects.filter(members__user=self.request.user).distinct().order_by('-id')


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
                'Изменять группу могут только владелец или администратор.'
            )

        serializer.save()

    def delete(self, request, *args, **kwargs):
        group = get_object_or_404(
            Group,
            pk=kwargs['pk'],
            members__user=request.user
        )

        if group.owner_id != request.user.id:
            raise PermissionDenied(
                'Удалить группу может только владелец.'
            )

        group.delete()
        from rest_framework.response import Response
        from rest_framework import status
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_group(self):
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
                'Ты не являешься участником этой группы.'
            )

        return group

    def get_queryset(self):
        group = self.get_group()

        return GroupMessage.objects.filter(
            group=group
        ).select_related('user').order_by('cr_at', 'id')

    def perform_create(self, serializer):
        group = self.get_group()

        serializer.save(
            group=group,
            user=self.request.user
        )
