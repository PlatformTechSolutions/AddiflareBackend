import graphene
from graphene_django_subscriptions.subscription import Subscription
from .serializers import MessageSerializer

class MessageSubscription(Subscription):
    class Meta:
        serializer_class = MessageSerializer
        stream = 'msg'
        description = 'Msg Subscription'
