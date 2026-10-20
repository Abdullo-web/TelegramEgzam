from rest_framework import serializers
from .models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id','owner','title','description','type','cr_at','link',]
        read_only_fields = ['id','owner','cr_at','link',]