from rest_framework import serializers

from . models import Message

class MessageSerializer(serializers.Serializer):
    room_name = serializers.CharField(max_length=100)
    msg = serializers.StringRelatedField(many=True)

    class Meta:
        model = Message
        fields = ['room_name', 'msg']

