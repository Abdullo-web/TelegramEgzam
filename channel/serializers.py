from rest_framework import serializers
from .models import Channel,Post


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id','owner','title','description','type','cr_at','link',]
        read_only_fields = ['id','owner','cr_at','link',]
        
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','description','channel','content','cr_at',]
        read_only_fields = ['id', 'channel', 'cr_at']